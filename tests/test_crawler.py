# tests for crawler.py

import pytest
from unittest.mock import patch, MagicMock
from src.crawler import crawl


def make_mock_response(html, status=200):
    """Helper to create a fake HTTP response."""
    mock = MagicMock()
    mock.status_code = status
    mock.text = html
    mock.raise_for_status = MagicMock()
    return mock


# Simple page with one link to a second page
MOCK_PAGE_1 = """
<html><body>
  <p>Hello world this is page one</p>
  <a href="/page/2/">Next</a>
</body></html>
"""

MOCK_PAGE_2 = """
<html><body>
  <p>This is page two with different words</p>
</body></html>
"""


@patch("src.crawler.time.sleep")  # stops tests from actually waiting 6 seconds
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
def test_crawl_extracts_text(mock_get, mock_sleep):
    mock_get.return_value = make_mock_response(MOCK_PAGE_1)

    pages = crawl("https://quotes.toscrape.com/")

    first_page_text = list(pages.values())[0]
    assert "Hello world" in first_page_text


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_respects_politeness(mock_get, mock_sleep):
    mock_get.side_effect = [
        make_mock_response(MOCK_PAGE_1),
        make_mock_response(MOCK_PAGE_2),
    ]

    crawl("https://quotes.toscrape.com/")

    # sleep must have been called with 6 seconds
    mock_sleep.assert_called_with(6)


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_handles_network_error(mock_get, mock_sleep):
    import requests as req
    mock_get.side_effect = req.exceptions.RequestException("Connection failed")

    # Should not crash, just return empty
    pages = crawl("https://quotes.toscrape.com/")
    assert isinstance(pages, dict)


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_no_duplicate_visits(mock_get, mock_sleep):
    # Page links back to itself - should only visit once
    LOOPING_PAGE = """
    <html><body>
      <p>Some content</p>
      <a href="/">Home</a>
    </body></html>
    """
    mock_get.return_value = make_mock_response(LOOPING_PAGE)

    pages = crawl("https://quotes.toscrape.com/")
    assert len(pages) == 1