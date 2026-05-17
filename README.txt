────────────────────────────────────────────────────────────────────────────────


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  REPOSITORY OVERVIEW                                                       │
  └────────────────────────────────────────────────────────────────────────────┘

    This repository is a curated collection of small, focused Python utilities
    centred around document processing and graphical image transformation. Also
    authored by Simon Chabrol and released under the MIT License, it is 100%
    Python and currently contains 16 commits — a newer, more targeted effort
    than the JavaScript repository.

    Description: 'Several small Python projects (graphical transformation,
    scraping...)'

    URL: https://github.com/simonchabrol/python-projects


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  PURPOSE & DESIGN PHILOSOPHY                                               │
  └────────────────────────────────────────────────────────────────────────────┘

    Where the JavaScript repository prioritises breadth across backend
    engineering domains, python-projects prioritises depth within a narrower
    niche: the programmatic manipulation of documents (PDFs) and images. This
    reflects one of Python's greatest strengths — its extraordinary ecosystem
    for file processing, image manipulation, and web scraping, embodied by
    libraries like Pillow, PyMuPDF, and BeautifulSoup.

    Each module solves a concrete, practical problem that a developer or non-
    technical user might encounter in daily work: converting a scanned PDF to
    grayscale before archiving, splitting a book PDF into chapters, or applying
    an artistic filter to a photograph. This pragmatic focus makes the
    repository immediately useful rather than purely academic.


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  MODULE DIRECTORY                                                          │
  └────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────┬──────────────────────────────────────────────┐
  │            MODULE            │                 DESCRIPTION                  │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ bw_transform_pdf             │ Applies grayscale transformation to each PDF │
  │                              │ page, reducing file size and preparing       │
  │                              │ documents for printing or archiving.         │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ html_parsing_demo            │ Demonstrates web scraping and HTML parsing   │
  │                              │ techniques using Python libraries such as    │
  │                              │ BeautifulSoup, extracting structured data    │
  │                              │ from web pages.                              │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ linocut                      │ Applies artistic filters inspired by linocut │
  │                              │ printmaking — high-contrast edge detection   │
  │                              │ and posterisation — to images using          │
  │                              │ PIL/Pillow.                                  │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ split_pdf_book               │ Splits a multi-page PDF (e.g. a scanned      │
  │                              │ book) into individual pages or logical       │
  │                              │ sections for easier navigation or            │
  │                              │ redistribution.                              │
  └──────────────────────────────┴──────────────────────────────────────────────┘


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  KEY TECHNICAL HIGHLIGHTS                                                  │
  └────────────────────────────────────────────────────────────────────────────┘


  ▸ PDF Processing
  ──────────────────

    Two of the four modules — bw_transform_pdf and split_pdf_book — deal with
    PDF manipulation. PDF is a notoriously complex format to work with
    programmatically: it encodes page layout, fonts, and images in a binary
    structure requiring specialised libraries to parse and transform. Their
    presence signals proficiency with Python's document processing ecosystem,
    likely via libraries such as PyMuPDF (fitz), pikepdf, or pypdf.


  ▸ Artistic Image Processing — the Linocut Effect
  ──────────────────────────────────────────────────

    The linocut module is the most creatively distinctive project in the
    repository. Linocut is a traditional printmaking technique that produces
    high-contrast, graphic images with bold outlines and a limited tonal range.
    Replicating this aesthetic in code requires a combination of techniques:
    edge detection (Canny or Sobel filters), colour quantisation (palette
    reduction), and potentially morphological operations to thicken lines. This
    module demonstrates not only technical Python skills but also a genuine
    understanding of digital image processing theory.


  ▸ Web Scraping
  ────────────────

    The html_parsing_demo covers one of Python's most iconic use cases. HTML
    parsing with BeautifulSoup or lxml is a foundational skill for data
    extraction, automated testing, and building data pipelines from web sources.
    Even as a demonstration, this module illustrates familiarity with the full
    web scraping workflow: HTTP request handling, HTML tree traversal, data
    extraction, and output formatting.


────────────────────────────────────────────────────────────────────────────────


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  PRÉSENTATION DU DÉPÔT                                                     │
  └────────────────────────────────────────────────────────────────────────────┘

    Ce dépôt est une collection de petits utilitaires Python focalisés, centrés
    sur le traitement de documents et la transformation graphique d'images.
    Également signé Simon Chabrol et distribué sous licence MIT, il est écrit à
    100 % en Python et compte 16 commits — un effort plus récent et plus ciblé
    que le dépôt JavaScript.

    Description : 'Several small Python projects (graphical transformation,
    scraping...)'

    URL : https://github.com/simonchabrol/python-projects


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  OBJECTIF & PHILOSOPHIE DE CONCEPTION                                      │
  └────────────────────────────────────────────────────────────────────────────┘

    Là où le dépôt JavaScript privilégie la largeur — couvrant un grand nombre
    de domaines backend —, python-projects privilégie la profondeur dans une
    niche plus étroite : la manipulation programmatique de documents PDF et
    d'images. Cela reflète l'une des grandes forces de Python — son
    extraordinaire écosystème pour le traitement de fichiers, la manipulation
    d'images et le scraping web, incarné par des bibliothèques comme Pillow,
    PyMuPDF ou BeautifulSoup.

    Chaque module résout un problème concret et pratique qu'un développeur ou un
    utilisateur non-technique pourrait rencontrer au quotidien : convertir un
    PDF scanné en niveaux de gris avant archivage, découper un livre PDF en
    chapitres, ou appliquer un filtre artistique à une photographie. Cette
    orientation pragmatique rend le dépôt immédiatement utile plutôt que
    purement académique.


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  RÉPERTOIRE DES MODULES                                                    │
  └────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────┬──────────────────────────────────────────────┐
  │            MODULE            │                 DESCRIPTION                  │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ bw_transform_pdf             │ Applique une transformation en niveaux de    │
  │                              │ gris à chaque page d'un PDF, réduisant la    │
  │                              │ taille et préparant l'impression ou          │
  │                              │ l'archivage.                                 │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ html_parsing_demo            │ Démontre le scraping web et le parsing HTML  │
  │                              │ avec des bibliothèques comme BeautifulSoup   │
  │                              │ pour extraire des données structurées.       │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ linocut                      │ Applique des filtres artistiques inspirés de │
  │                              │ la linogravure (détection de contours,       │
  │                              │ postérisation) à des images via PIL/Pillow.  │
  ├──────────────────────────────┼──────────────────────────────────────────────┤
  │ split_pdf_book               │ Découpe un PDF multi-pages (ex. livre        │
  │                              │ scanné) en pages individuelles ou sections   │
  │                              │ logiques pour faciliter la navigation.       │
  └──────────────────────────────┴──────────────────────────────────────────────┘


  ┌────────────────────────────────────────────────────────────────────────────┐
  │  POINTS TECHNIQUES SAILLANTS                                               │
  └────────────────────────────────────────────────────────────────────────────┘


  ▸ Traitement de PDF
  ─────────────────────

    Deux des quatre modules — bw_transform_pdf et split_pdf_book — traitent de
    la manipulation de PDF. Le format PDF est notoirement complexe à manipuler
    par programme : il encode la mise en page, les polices et les images dans
    une structure binaire nécessitant des bibliothèques spécialisées pour être
    analysée et transformée. Leur présence signale une maîtrise de l'écosystème
    de traitement de documents Python, vraisemblablement via des bibliothèques
    comme PyMuPDF (fitz), pikepdf ou pypdf.


  ▸ Traitement d'image artistique — l'effet linogravure
  ───────────────────────────────────────────────────────

    Le module linocut est le projet le plus distinctif créativement dans le
    dépôt. La linogravure est une technique d'impression traditionnelle qui
    produit des images graphiques à fort contraste, aux contours marqués et à la
    gamme tonale limitée. Reproduire cet effet en code nécessite une combinaison
    de techniques : détection de contours (filtres de Canny ou Sobel),
    quantification des couleurs (réduction de la palette), et potentiellement
    des opérations morphologiques pour épaissir les traits. Ce module démontre
    non seulement des compétences Python techniques, mais aussi une véritable
    compréhension de la théorie du traitement numérique de l'image.


  ▸ Scraping web
  ────────────────

    Le module html_parsing_demo couvre l'un des cas d'usage les plus
    emblématiques de Python. Le parsing HTML avec BeautifulSoup ou lxml est une
    compétence fondamentale pour l'extraction de données, les tests automatisés
    et la construction de pipelines de données à partir de sources web. Même en
    tant que démo, ce module illustre la familiarité du développeur avec le
    workflow complet du scraping web : gestion des requêtes HTTP, traversée de
    l'arbre HTML, extraction de données et formatage des sorties.


────────────────────────────────────────────────────────────────────────────────
