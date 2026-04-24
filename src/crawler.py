# crawler.py - Handles web crawling for the search engine

import requests
from bs4 import BeautifulSoup
import time


def crawl(base_url="https://quotes.toscrape.com/"):
    """
    Crawls all pages of the target website and returns their text content.
    Respects a 6-second politeness window between requests.
    
    Returns:
        dict: {url: text_content} for every page visited
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
            response.raise_for_status()  # catches 404s, 500s etc

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            visited.add(url)
            continue

        visited.add(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract visible text from the page
        pages[url] = soup.get_text(separator=" ", strip=True)

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