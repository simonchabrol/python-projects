"""
sketch_filter.py — Engraving/linocut filter applied to images

Structure attendue :
    input_images/    ← Input images
    output_sketchs/  ← Output images

pip install opencv-python numpy
"""

import cv2
import numpy as np
import argparse
import sys
from pathlib import Path


INPUT_DIR  = Path("input_images")
OUTPUT_DIR = Path("output_sketchs")

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}


def process_directory(
    input_dir: Path = INPUT_DIR,
    output_dir: Path = OUTPUT_DIR,
    style: str = "linocut",
    detail_level: float = 1.0,
    contrast: float = 1.2,
    invert: bool = False,
) -> None:
    """
    Traite toutes les images du répertoire input_dir et enregistre
    les résultats dans output_dir en conservant les noms de fichiers.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Répertoire source introuvable : {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    images = [p for p in sorted(input_dir.iterdir()) if p.suffix.lower() in SUPPORTED_EXTENSIONS]

    if not images:
        print(f"Aucune image trouvée dans « {input_dir} ».")
        return

    print(f"Traitement de {len(images)} image(s) — style : {style}\n")
    errors = 0

    for img_path in images:
        output_path = output_dir / img_path.name
        try:
            apply_sketch_filter(
                input_path=str(img_path),
                output_path=str(output_path),
                style=style,
                detail_level=detail_level,
                contrast=contrast,
                invert=invert,
            )
        except Exception as e:
            print(f"  ✗ Erreur pour {img_path.name} : {e}", file=sys.stderr)
            errors += 1

    print(f"\n{'─' * 40}")
    print(f"Terminé : {len(images) - errors}/{len(images)} image(s) converties → {output_dir}/")
    if errors:
        print(f"  ✗ {errors} erreur(s) rencontrée(s).")


def apply_sketch_filter(
    input_path: str,
    output_path: str = None,
    style: str = "linocut",
    detail_level: float = 1.0,
    contrast: float = 1.2,
    invert: bool = False,
) -> str:
    """
    Applique un filtre sketch/gravure à une image.

    Paramètres
    ----------
    input_path   : chemin vers l'image source
    output_path  : chemin de sortie (auto si None)
    style        : "linocut"   → gravure sur bois dense (comme vos exemples)
                   "pencil"    → croquis au crayon
                   "engraving" → gravure fine, hachures régulières
    detail_level : 0.5 à 2.0, quantité de détail préservé (défaut 1.0)
    contrast     : multiplicateur de contraste final (défaut 1.2)

    Retourne
    --------
    Le chemin du fichier de sortie.
    """
    # ── 1. Chargement ────────────────────────────────────────────────────────
    img_bgr = cv2.imread(input_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Impossible de lire : {input_path}")

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # ── 2. Pré-traitement : réduction du bruit ────────────────────────────────
    denoised = cv2.fastNlMeansDenoising(gray, h=7, templateWindowSize=7, searchWindowSize=21)

    # ── 3. Rendu selon le style ───────────────────────────────────────────────
    if style == "linocut":
        result = _linocut_style(denoised, detail_level)

    elif style == "pencil":
        result = _pencil_style(denoised, detail_level)

    elif style == "engraving":
        result = _engraving_style(denoised, detail_level)

    elif style == "printing":
        result = _printing_style(denoised, detail_level)

    else:
        raise ValueError(f"Style inconnu : {style!r}. Choisir parmi linocut, pencil, engraving, printing.")

    # ── 4. Post-traitement : contraste & niveaux ──────────────────────────────
    result = _adjust_contrast(result, contrast)

    # ── 4b. Inversion optionnelle (noir↔blanc) ────────────────────────────────
    if invert:
        result = cv2.bitwise_not(result)

    # ── 5. Sauvegarde ─────────────────────────────────────────────────────────
    if output_path is None:
        p = Path(input_path)
        output_path = str(p.parent / f"{p.stem}_sketch_{style}{p.suffix}")

    cv2.imwrite(output_path, result)
    print(f"✓ Image sauvegardée : {output_path}")
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# Styles internes
# ─────────────────────────────────────────────────────────────────────────────

def _linocut_style(gray: np.ndarray, detail: float) -> np.ndarray:
    """
    Rendu linogravure : zones de noir très denses séparées par des lignes
    blanches nettes — fidèle à vos exemples (hélicoptère, paysage).
    """
    h, w = gray.shape

    # Flou bilatéral : préserve les bords tout en lissant les textures
    sigma = max(1, int(15 / detail))
    smooth = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=sigma)

    # Rehaussement des bords (Unsharp Mask)
    blur = cv2.GaussianBlur(smooth, (0, 0), sigmaX=2.0 / detail)
    sharp = cv2.addWeighted(smooth, 1.5, blur, -0.5, 0)

    # Détection des bords (Laplacien) pour renforcer les contours gravés
    laplacian = cv2.Laplacian(sharp, cv2.CV_64F, ksize=3)
    edge_mask = np.clip(np.abs(laplacian) / 40.0, 0, 1)

    # Seuillage adaptatif → texture hachurée dense
    block = max(11, int(31 / detail))
    if block % 2 == 0:
        block += 1
    thresh = cv2.adaptiveThreshold(
        sharp, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=block,
        C=int(8 * detail),
    )

    # Combinaison : renforcer les bords dans le masque seuillé
    edge_darken = (edge_mask * 180).astype(np.uint8)
    result = cv2.subtract(thresh, edge_darken)

    # Érosion légère pour épaissir les traits noirs (look gravure)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    result = cv2.erode(result, kernel, iterations=1)

    return result


def _pencil_style(gray: np.ndarray, detail: float) -> np.ndarray:
    """
    Croquis au crayon classique : traits fins sur fond blanc.
    """
    # Inversion + flou gaussien
    inv = cv2.bitwise_not(gray)
    sigma = max(1, int(21 / detail))
    if sigma % 2 == 0:
        sigma += 1
    blurred_inv = cv2.GaussianBlur(inv, (sigma, sigma), 0)

    # Division pour obtenir les traits
    sketch = cv2.divide(gray, 255 - blurred_inv, scale=256.0)
    sketch = np.clip(sketch, 0, 255).astype(np.uint8)

    # Renforcement des traits sombres
    _, sketch = cv2.threshold(sketch, 230, 255, cv2.THRESH_TRUNC)
    sketch = cv2.normalize(sketch, None, 0, 255, cv2.NORM_MINMAX)

    return sketch


def _engraving_style(gray: np.ndarray, detail: float) -> np.ndarray:
    """
    Gravure fine : hachures régulières simulant une taille-douce.
    """
    # Flou pour lisser avant quantification
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Gradient de luminosité
    grad_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)

    # Zones sombres → hachures denses
    h, w = gray.shape
    lines = np.ones((h, w), dtype=np.uint8) * 255
    spacing = max(3, int(6 / detail))
    for y in range(0, h, spacing):
        cv2.line(lines, (0, y), (w, y + 10), 0, 1)

    # Masquer les hachures selon la luminosité : zones sombres = plus de hachures
    threshold = 128
    dark_mask = (blur < threshold).astype(np.uint8) * 255
    hatch_layer = cv2.bitwise_and(lines, lines, mask=cv2.bitwise_not(dark_mask))

    # Bords détectés → contours nets
    edges = cv2.Canny(blur, 50, 150)
    edges_dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)

    # Fusion
    result = cv2.bitwise_and(hatch_layer, cv2.bitwise_not(edges_dilated))
    result = np.clip(result, 0, 255).astype(np.uint8)

    return result


def _printing_style(gray: np.ndarray, detail: float) -> np.ndarray:
    """
    Négatif d'imprimerie noir et blanc : seuillage dur après égalisation
    d'histogramme, puis inversion. Les zones sombres deviennent des plages
    noires opaques et denses, les lumières créent des trouées blanches nettes
    — proche d'un cliché typographique ou d'une plaque offset.
    """
    # Égalisation d'histogramme → exploit toute la dynamique
    equalized = cv2.equalizeHist(gray)

    # Flou bilatéral : lisse sans détruire les bords
    sigma = max(1, int(12 / detail))
    smooth = cv2.bilateralFilter(equalized, d=9, sigmaColor=80, sigmaSpace=sigma)

    # Unsharp mask : accentue les transitions
    blur = cv2.GaussianBlur(smooth, (0, 0), sigmaX=2.0 / detail)
    sharp = cv2.addWeighted(smooth, 1.8, blur, -0.8, 0)

    # Seuillage adaptatif avec bloc large → grandes zones homogènes
    block = max(15, int(51 / detail))
    if block % 2 == 0:
        block += 1
    thresh = cv2.adaptiveThreshold(
        sharp, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=block,
        C=int(6 * detail),
    )

    # Inversion : noir là où la photo était sombre (logique plaque d'impression)
    inverted = cv2.bitwise_not(thresh)

    # Fermeture morphologique : comble les trous dans les plages noires
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closed = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel_close, iterations=1)

    # Réinjection des contours nets par-dessus les plages
    edges = cv2.Canny(sharp, 30, 100)
    edges_dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
    result = cv2.bitwise_or(closed, edges_dilated)

    return result


def _adjust_contrast(img: np.ndarray, factor: float) -> np.ndarray:
    """Ajustement simple du contraste autour du point médian."""
    if factor == 1.0:
        return img
    img_float = img.astype(np.float32)
    adjusted = (img_float - 128) * factor + 128
    return np.clip(adjusted, 0, 255).astype(np.uint8)


# ─────────────────────────────────────────────────────────────────────────────
# Interface en ligne de commande
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Applique un filtre sketch/gravure à toutes les images de input_images/ "
            "et enregistre les résultats dans output_sketchs/."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples
--------
  # Utilisation standard (linocut, répertoires par défaut) :
  python sketch_filter.py

  # Croquis au crayon :
  python sketch_filter.py --style pencil

  # Gravure fine avec plus de détail et contraste renforcé :
  python sketch_filter.py --style engraving --detail 1.5 --contrast 1.4

  # Négatif d'imprimerie (plaque typographique) :
  python sketch_filter.py --style printing

  # Répertoires personnalisés :
  python sketch_filter.py --input mes_photos --output mes_sketchs
        """,
    )
    parser.add_argument(
        "--input", default=str(INPUT_DIR),
        help=f"Répertoire source (défaut : {INPUT_DIR})"
    )
    parser.add_argument(
        "--output", default=str(OUTPUT_DIR),
        help=f"Répertoire de sortie (défaut : {OUTPUT_DIR})"
    )
    parser.add_argument(
        "--style", default="linocut",
        choices=["linocut", "pencil", "engraving", "printing"],
        help="Style du rendu (défaut : linocut)"
    )
    parser.add_argument(
        "--detail", type=float, default=1.0,
        help="Niveau de détail, 0.5–2.0 (défaut : 1.0)"
    )
    parser.add_argument(
        "--contrast", type=float, default=1.2,
        help="Contraste final, 0.5–2.0 (défaut : 1.2)"
    )
    parser.add_argument(
        "--invert", action="store_true",
        help="Inverse le rendu final (noir↔blanc)"
    )

    args = parser.parse_args()

    try:
        process_directory(
            input_dir=Path(args.input),
            output_dir=Path(args.output),
            style=args.style,
            detail_level=args.detail,
            contrast=args.contrast,
            invert=args.invert,
        )
    except FileNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
