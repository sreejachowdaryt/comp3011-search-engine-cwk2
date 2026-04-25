# tests for crawler.py

import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.crawler import crawl, extract_page_content


def make_mock_response(html, status=200):
    """Helper to create a fake HTTP response."""
    mock = MagicMock()
    mock.status_code = status
    mock.text = html
    mock.raise_for_status = MagicMock()
    return mock


# Mock pages using the actual quotes.toscrape.com HTML structure
MOCK_PAGE_1 = """
<html><body>
  <div class="quote">
    <span class="text">The world is beautiful and worth fighting for.</span>
    <span class="author">Ernest Hemingway</span>
    <div class="tags">
      <a class="tag">love</a>
      <a class="tag">life</a>
    </div>
  </div>
  <a href="/page/2/">Next</a>
</body></html>
"""

MOCK_PAGE_2 = """
<html><body>
  <div class="quote">
    <span class="text">It is our choices that show what we truly are.</span>
    <span class="author">J.K. Rowling</span>
    <div class="tags">
      <a class="tag">choices</a>
      <a class="tag">character</a>
    </div>
  </div>
</body></html>
"""

MOCK_AUTHOR_PAGE = """
<html><body>
  <h3 class="author-title">Ernest Hemingway</h3>
  <div class="author-description">
    Ernest Miller Hemingway was an American novelist and short-story writer.
  </div>
</body></html>
"""

MOCK_PAGE_NO_QUOTES = """
<html><body>
  <p>Some random page with no quote structure</p>
</body></html>
"""


# ---------- extract_page_content() tests ----------

def test_extract_quote_text():
    soup = BeautifulSoup(MOCK_PAGE_1, "html.parser")
    content = extract_page_content(soup)
    assert "beautiful" in content


def test_extract_author_name():
    soup = BeautifulSoup(MOCK_PAGE_1, "html.parser")
    content = extract_page_content(soup)
    assert "Hemingway" in content


def test_extract_tags():
    soup = BeautifulSoup(MOCK_PAGE_1, "html.parser")
    content = extract_page_content(soup)
    assert "love" in content
    assert "life" in content


def test_extract_author_page_description():
    soup = BeautifulSoup(MOCK_AUTHOR_PAGE, "html.parser")
    content = extract_page_content(soup)
    assert "novelist" in content


def test_extract_author_page_title():
    soup = BeautifulSoup(MOCK_AUTHOR_PAGE, "html.parser")
    content = extract_page_content(soup)
    assert "Hemingway" in content


def test_extract_falls_back_to_body_when_no_quotes():
    soup = BeautifulSoup(MOCK_PAGE_NO_QUOTES, "html.parser")
    content = extract_page_content(soup)
    assert "random" in content


def test_extract_returns_string():
    soup = BeautifulSoup(MOCK_PAGE_1, "html.parser")
    content = extract_page_content(soup)
    assert isinstance(content, str)


def test_extract_excludes_navigation_text():
    # Navigation text like "Next", "Login" should not dominate
    # since we only extract quote-specific elements
    html = """
    <html><body>
      <nav>Login Next Previous Top Ten Tags</nav>
      <div class="quote">
        <span class="text">A beautiful quote here.</span>
        <span class="author">Some Author</span>
        <div class="tags"><a class="tag">wisdom</a></div>
      </div>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
    content = extract_page_content(soup)
    assert "beautiful" in content
    assert "wisdom" in content
    # Navigation text should not be in extracted content
    assert "Login" not in content
    assert "Previous" not in content


# ---------- crawl() tests ----------

@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_returns_pages(mock_get, mock_sleep):
    mock_get.side_effect = [
        make_mock_response(MOCK_PAGE_1),
        make_mock_response(MOCK_PAGE_2),
    ]
    pages = crawl("https://quotes.toscrape.com/")
    assert len(pages) == 2


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_extracts_meaningful_text(mock_get, mock_sleep):
    mock_get.return_value = make_mock_response(MOCK_PAGE_1)
    pages = crawl("https://quotes.toscrape.com/")
    first_page_text = list(pages.values())[0]
    assert "beautiful" in first_page_text
    assert "Hemingway" in first_page_text


def test_crawl_extracts_tags():
    soup = BeautifulSoup(MOCK_PAGE_1, "html.parser")
    content = extract_page_content(soup)
    assert "love" in content
    assert "life" in content


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_respects_politeness(mock_get, mock_sleep):
    mock_get.side_effect = [
        make_mock_response(MOCK_PAGE_1),
        make_mock_response(MOCK_PAGE_2),
    ]
    crawl("https://quotes.toscrape.com/")
    mock_sleep.assert_called_with(6)


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_handles_network_error(mock_get, mock_sleep):
    import requests as req
    mock_get.side_effect = req.exceptions.RequestException("Connection failed")
    pages = crawl("https://quotes.toscrape.com/")
    assert isinstance(pages, dict)


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_no_duplicate_visits(mock_get, mock_sleep):
    LOOPING_PAGE = """
    <html><body>
      <div class="quote">
        <span class="text">Do not go gentle into that good night.</span>
        <span class="author">Dylan Thomas</span>
        <div class="tags"><a class="tag">life</a></div>
      </div>
      <a href="/">Home</a>
    </body></html>
    """
    mock_get.return_value = make_mock_response(LOOPING_PAGE)
    pages = crawl("https://quotes.toscrape.com/")
    assert len(pages) == 1


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_only_follows_internal_links(mock_get, mock_sleep):
    EXTERNAL_LINK_PAGE = """
    <html><body>
      <div class="quote">
        <span class="text">Some quote text here.</span>
        <span class="author">Some Author</span>
        <div class="tags"><a class="tag">wisdom</a></div>
      </div>
      <a href="https://external.com/page">External</a>
      <a href="/internal/page">Internal</a>
    </body></html>
    """
    INTERNAL_PAGE = """
    <html><body>
      <div class="quote">
        <span class="text">Another quote text.</span>
        <span class="author">Another Author</span>
        <div class="tags"><a class="tag">life</a></div>
      </div>
    </body></html>
    """
    mock_get.side_effect = [
        make_mock_response(EXTERNAL_LINK_PAGE),
        make_mock_response(INTERNAL_PAGE),
    ]
    pages = crawl("https://quotes.toscrape.com/")
    # Should visit base URL + internal page, not external
    assert len(pages) == 2


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_returns_dict(mock_get, mock_sleep):
    mock_get.return_value = make_mock_response(MOCK_PAGE_1)
    pages = crawl("https://quotes.toscrape.com/")
    assert isinstance(pages, dict)


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_handles_404(mock_get, mock_sleep):
    import requests as req
    mock = make_mock_response("", status=404)
    mock.raise_for_status.side_effect = req.exceptions.HTTPError("404")
    mock_get.return_value = mock
    pages = crawl("https://quotes.toscrape.com/")
    assert isinstance(pages, dict)