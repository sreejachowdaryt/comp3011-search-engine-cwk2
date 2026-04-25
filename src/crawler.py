# crawler.py - Handles web crawling for the search engine

import requests
from bs4 import BeautifulSoup
import time


def extract_page_content(soup: BeautifulSoup) -> str:
    """
    Extracts only meaningful content from a page — quotes, authors,
    and tags. Ignores navigation, footers, and boilerplate text that
    appears on every page and would pollute the index.

    Args:
        soup (BeautifulSoup): Parsed HTML of the page

    Returns:
        str: Clean text content from meaningful page elements only

    Time complexity:  O(n) where n = number of HTML elements
    Space complexity: O(t) where t = total text length extracted
    """
    content_parts = []

    # Extract quote text
    for quote in soup.select(".quote .text"):
        content_parts.append(quote.get_text(strip=True))

    # Extract author names
    for author in soup.select(".quote .author"):
        content_parts.append(author.get_text(strip=True))

    # Extract tags
    for tag in soup.select(".quote .tags .tag"):
        content_parts.append(tag.get_text(strip=True))

    # For author biography pages extract the description
    for bio in soup.select(".author-description"):
        content_parts.append(bio.get_text(strip=True))

    # For author pages extract the name and born details
    for name in soup.select(".author-title"):
        content_parts.append(name.get_text(strip=True))

    # If no structured content found fall back to body text
    # This handles any unexpected page structures
    if not content_parts:
        body = soup.find("body")
        if body:
            return body.get_text(separator=" ", strip=True)

    return " ".join(content_parts)


def crawl(base_url: str = "https://quotes.toscrape.com/") -> dict[str, str]:
    """
    Crawls all pages of the target website and returns their text content.
    Respects a 6-second politeness window between requests.
    Only extracts meaningful content (quotes, authors, tags) to avoid
    polluting the index with navigation and boilerplate text.

    Args:
        base_url (str): The starting URL to crawl from

    Returns:
        dict: {url: text_content} for every page visited

    Time complexity:  O(p * l) where p = number of pages,
                      l = average links per page
    Space complexity: O(p) for storing visited pages and queue
    """
    visited = set()
    to_visit = [base_url]
    pages = {}

    print(f"Starting crawl from: {base_url}")

    while to_visit:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            print(f"Crawling: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            visited.add(url)
            continue

        visited.add(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract only meaningful content, not navigation/footer
        pages[url] = extract_page_content(soup)

        # Find all internal links and add to queue
        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Only follow internal links
            if href.startswith("/"):
                full_url = base_url.rstrip("/") + href
                if full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)

        # Politeness window - mandatory 6 second wait
        if to_visit:
            print(f"Waiting 6 seconds before next request...")
            time.sleep(6)

    print(f"Crawl complete. {len(pages)} pages found.")
    return pages