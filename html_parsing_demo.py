"""
Educational HTML Parsing Demo
-----------------------------

This script demonstrates how to:

- parse a locally exported HTML file,
- extract post links,
- retrieve publicly accessible image URLs,
- download images locally.

The goal is educational only.

Users are responsible for respecting:
- platform Terms of Service,
- copyright laws,
- privacy regulations,
- applicable local laws.

Tested with:
- Python 3.10+
"""

from bs4 import BeautifulSoup
import requests
import os
import re
import json
import time
import logging


# ============================================================================
# CONFIGURATION
# ============================================================================

# Exported HTML file
HTML_FILE = "saved_posts.html"

# Output directory
OUTPUT_DIR = "downloads"

# Optional section filter
# Example: ["example"]
TARGET_SECTIONS = [
    "TEST"
]

# Delay between requests (seconds)
REQUEST_DELAY = 2

# Maximum number of posts to process
MAX_DOWNLOADS = 50


# ============================================================================
# INITIALIZATION
# ============================================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ============================================================================
# HTML PARSING
# ============================================================================

def load_html(file_path):
    """
    Load and parse the exported HTML file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return BeautifulSoup(file.read(), "html.parser")


def extract_post_links(soup, target_sections):
    """
    Extract post links from selected sections.
    """
    links = []
    seen = set()

    sections = soup.find_all(
        "h2",
        class_="_3-95 _2pim _a6-h _a6-i"
    )

    for section in sections:
        section_name = section.get_text(strip=True)

        # Filter sections
        if any(keyword.lower() in section_name.lower()
               for keyword in target_sections):

            logging.info(f"Section found: {section_name}")

            parent = section.find_parent()

            for anchor in parent.find_all("a", href=True):
                href = anchor["href"]

                if "/p/" in href and href not in seen:
                    links.append(href)
                    seen.add(href)

    return links


# ============================================================================
# IMAGE EXTRACTION
# ============================================================================

def extract_image_urls(html_content):
    """
    Extract image URLs from page HTML.

    The script first tries to read embedded JSON metadata.
    If unavailable, it falls back to Open Graph metadata.
    """
    image_urls = []

    try:
        match = re.search(
            r'window\._sharedData = (.*?);</script>',
            html_content
        )

        if match:
            data = json.loads(match.group(1))

            media = (
                data["entry_data"]["PostPage"][0]
                ["graphql"]["shortcode_media"]
            )

            # Single image
            if "display_url" in media:
                image_urls.append(media["display_url"])

            # Multiple images
            if "edge_sidecar_to_children" in media:
                for edge in media["edge_sidecar_to_children"]["edges"]:
                    image_urls.append(edge["node"]["display_url"])

    except Exception:
        pass

    # Fallback using Open Graph image
    if not image_urls:
        soup = BeautifulSoup(html_content, "html.parser")

        meta = soup.find("meta", property="og:image")

        if meta:
            image_urls.append(meta.get("content"))

    return image_urls


# ============================================================================
# DOWNLOAD UTILITIES
# ============================================================================

def download_image(url, output_path):
    """
    Download an image and save it locally.
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if (
        response.status_code == 200 and
        len(response.content) > 10000
    ):
        with open(output_path, "wb") as file:
            file.write(response.content)

        return True

    return False


# ============================================================================
# MAIN PROCESS
# ============================================================================

def main():

    logging.info("Loading HTML export...")

    soup = load_html(HTML_FILE)

    logging.info("Extracting links...")

    post_links = extract_post_links(
        soup,
        TARGET_SECTIONS
    )

    logging.info(f"{len(post_links)} post(s) found")

    processed = 0

    for index, post_url in enumerate(post_links):

        if processed >= MAX_DOWNLOADS:
            logging.info("Maximum download limit reached")
            break

        logging.info(f"Processing: {post_url}")

        try:
            response = requests.get(
                post_url,
                headers=HEADERS,
                timeout=10
            )

            image_urls = extract_image_urls(response.text)

            if not image_urls:
                logging.warning("No image found")
                continue

            for image_index, image_url in enumerate(image_urls):

                filename = os.path.join(
                    OUTPUT_DIR,
                    f"img_{index}_{image_index}.jpg"
                )

                success = download_image(
                    image_url,
                    filename
                )

                if success:
                    logging.info(f"Saved: {filename}")
                else:
                    logging.warning(
                        f"Download failed: {image_url}"
                    )

            processed += 1

            # Small delay between requests
            time.sleep(REQUEST_DELAY)

        except Exception as error:
            logging.error(f"Error: {error}")

    logging.info("Finished")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
