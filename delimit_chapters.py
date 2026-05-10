import fitz
import re
import unicodedata

PDF_PATH = "A PSYCHOSEXUAL JOURNEY— (7 ESSAYS + 3) + 1 ≈ BIRTH_MAY_2026_print_.pdf"

def normalize_text(s):

    s = unicodedata.normalize("NFKD", s)

    s = "".join(
        c for c in s
        if not unicodedata.combining(c)
    )

    s = s.replace("—", "-")
    s = s.replace("–", "-")

    s = " ".join(s.split())

    return s.upper()


CHAPTERS = [

    ("INTRODUCTION", "INTRODUCTION"),
    ("CHANGES TO THE BOOK — ÉVOLUTIONS DU RECUEIL", "CHANGES TO THE BOOK"),

    ("JANE AND I — A FICTIONAL ALTER EGO", "JANE AND I"),
    ("ALIEN (1979) — A SEXUAL SUBTEXT ?", "ALIEN"),

    ("TWO NOS BEFORE YES — REFLECTIONS ON MALE AND FEMALE LATE VIRGINITY", "TWO NOS BEFORE YES"),

    ("FRENCH CINEMA AND SEXUALITY — TEN ESSENTIAL FILMS (1966–2019)", "FRENCH CINEMA AND SEXUALITY"),

    ("THE SELF AS A FLAG — A MANIFESTO", "THE SELF AS A FLAG"),

    ("PROSTITUTION EN FRANCE — ENTRE HYPOCRISIE ET DIGNITÉ", "PROSTITUTION EN FRANCE"),

    ("ROBOCOP (1987) — MASCULINITY AND THE MACHINE", "ROBOCOP"),

    ("DEREK JARMAN — BRITISH AND QUEER CINEMA", "DEREK JARMAN"),

    ("SEX-ED — A COMPREHENSIVE HISTORY", "SEX-ED"),

    ("INTERSEX — HISTORY, SOCIETY AND SURGERY", "INTERSEX"),

    ("ARCHAIC MYTHS >> MODERN MINDS", "ARCHAIC MYTHS"),

    ("STELLAR WINDS — MORPHING DESIRE", "STELLAR WINDS"),

    ("KEROUAC AND THE MISSING MALE ARCHETYPE", "KEROUAC"),

    ("MALE AND FEMALE SEXUALITY — 77 YEARS AFTER THE KINSEY REPORTS", "MALE AND FEMALE SEXUALITY"),

    ("ANALOG DATING — A BRIEF HISTORY OF DATING SYSTEMS", "ANALOG DATING"),

    ("ED/SD — A MEDICAL HISTORY", "ED/SD"),

    ("SEXUAL GEOMETRY — ICONIC SEXUALITY MODELS", "SEXUAL GEOMETRY"),

    ("INNER SHELF — EARLY INFLUENCES", "INNER SHELF"),

    ("THE WHEATFIELD ON THE SOFA — AN INTRODUCTION TO PSYCHOANALYSIS", "THE WHEATFIELD"),

    ("ELLEN, OR ALWAYS ON TRIAL", "ELLEN"),

    ("40 WEEKS — PREGNANCY, OBSTETRICS AND NEONATOLOGY", "40 WEEKS"),

    ("CONCLUSION", "CONCLUSION"),

    ("BIBLIOGRAPHY", "BIBLIOGRAPHY"),
]

doc = fitz.open(PDF_PATH)

results = []

# IMPORTANT :
# on saute couverture + intro + sommaire
current_page = 9

for display_title, search_title in CHAPTERS:

    found_page = None

    search = normalize_text(search_title)

    for page_num in range(current_page, len(doc)):

        page = doc[page_num]

        text = normalize_text(
            page.get_text("text")
        )

        # recherche stricte :
        # le titre doit apparaître tôt dans la page
        first_part = text[:1200]

        if search in first_part:

            found_page = page_num + 1

            current_page = page_num + 1

            print(f"FOUND: {display_title} -> {found_page}")

            break

    if found_page:
        results.append((display_title, found_page))

# délimitations
final = []

for i, (title, start_page) in enumerate(results):

    if i < len(results) - 1:
        end_page = results[i + 1][1] - 1
    else:
        end_page = len(doc)

    final.append((title, start_page, end_page))

# affichage
print("\nCHAPTERS = [\n")

for title, start, end in final:

    safe = title

    safe = re.sub(r"[—,:?()»«!'.]", "", safe)
    safe = safe.replace("/", "_")
    safe = safe.replace(">>", "")
    safe = re.sub(r"\s+", "_", safe)
    safe = re.sub(r"_+", "_", safe)

    safe = safe.strip("_")

    print(f'    ("{safe}", {start}, {end}),')

print("\n]")
