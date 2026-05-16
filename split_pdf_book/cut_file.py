import fitz
import os

PDF_PATH = "A PSYCHOSEXUAL JOURNEY— (7 ESSAYS + 3) + 1 ≈ BIRTH_MAY_2026_print_.pdf"

OUTPUT_DIR = "chapters"

CHAPTERS = [

    ("INTRODUCTION", 47, 47),

    ("JANE_AND_I_A_FICTIONAL_ALTER_EGO", 48, 86),

    ("ALIEN_1979_A_SEXUAL_SUBTEXT", 87, 96),

    ("TWO_NOS_BEFORE_YES_REFLECTIONS_ON_MALE_AND_FEMALE_LATE_VIRGINITY",
     97, 106),

    ("FRENCH_CINEMA_AND_SEXUALITY_TEN_ESSENTIAL_FILMS_1966–2019",
     107, 116),

    ("THE_SELF_AS_A_FLAG_A_MANIFESTO",
     117, 134),

    ("PROSTITUTION_EN_FRANCE_ENTRE_HYPOCRISIE_ET_DIGNITÉ",
     135, 150),

    ("ROBOCOP_1987_MASCULINITY_AND_THE_MACHINE",
     151, 159),

    ("DEREK_JARMAN_BRITISH_AND_QUEER_CINEMA",
     160, 166),

    ("SEX-ED_A_COMPREHENSIVE_HISTORY",
     167, 181),

    ("INTERSEX_HISTORY_SOCIETY_AND_SURGERY",
     182, 197),

    ("ARCHAIC_MYTHS_MODERN_MINDS",
     198, 212),

    ("STELLAR_WINDS_MORPHING_DESIRE",
     213, 223),

    ("KEROUAC_AND_THE_MISSING_MALE_ARCHETYPE",
     224, 231),

    ("MALE_AND_FEMALE_SEXUALITY_77_YEARS_AFTER_THE_KINSEY_REPORTS",
     232, 239),

    ("ANALOG_DATING_A_BRIEF_HISTORY_OF_DATING_SYSTEMS",
     240, 252),

    ("ED_SD_A_MEDICAL_HISTORY",
     253, 261),

    ("SEXUAL_GEOMETRY_ICONIC_SEXUALITY_MODELS",
     262, 270),

    ("INNER_SHELF_EARLY_INFLUENCES",
     271, 273),

    ("THE_WHEATFIELD_ON_THE_SOFA_AN_INTRODUCTION_TO_PSYCHOANALYSIS",
     274, 287),

    ("ELLEN_OR_ALWAYS_ON_TRIAL",
     288, 324),

    ("40_WEEKS_PREGNANCY_OBSTETRICS_AND_NEONATOLOGY",
     325, 338),

    ("CONCLUSION",
     339, 340),

    ("BIBLIOGRAPHY",
     341, 346),
]

# ---------------------------------------------------
# création dossier output
# ---------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------
# ouverture PDF
# ---------------------------------------------------

doc = fitz.open(PDF_PATH)

# ---------------------------------------------------
# découpe
# ---------------------------------------------------

for title, start_page, end_page in CHAPTERS:

    new_doc = fitz.open()

    # pages PDF = index 0
    for page_num in range(start_page - 1, end_page):

        new_doc.insert_pdf(
            doc,
            from_page=page_num,
            to_page=page_num
        )

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{title}.pdf"
    )

    new_doc.save(output_path)

    new_doc.close()

    print(f"CREATED: {output_path}")

doc.close()

print("\nDONE.")
