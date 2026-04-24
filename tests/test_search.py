# tests for search.py

import pytest
from src.search import find_pages, print_index_entry


SAMPLE_INDEX = {
    "good": {
        "https://example.com/page1": {"frequency": 2, "positions": [0, 5], "tf_idf": 0.3},
        "https://example.com/page2": {"frequency": 1, "positions": [2], "tf_idf": 0.1},
    },
    "friends": {
        "https://example.com/page1": {"frequency": 1, "positions": [3], "tf_idf": 0.25},
    },
    "indifference": {
        "https://example.com/page3": {"frequency": 1, "positions": [7], "tf_idf": 0.5},
    },
}


# ---------- find_pages() tests ----------

def test_find_single_word():
    results = find_pages(SAMPLE_INDEX, "indifference")
    urls = [r[0] for r in results]
    assert "https://example.com/page3" in urls


def test_find_multi_word():
    results = find_pages(SAMPLE_INDEX, "good friends")
    urls = [r[0] for r in results]
    # Only page1 has both words
    assert "https://example.com/page1" in urls
    assert "https://example.com/page2" not in urls


def test_find_returns_ranked_results():
    results = find_pages(SAMPLE_INDEX, "good")
    # page1 has higher tf_idf so should come first
    assert results[0][0] == "https://example.com/page1"


def test_find_word_not_in_index():
    results = find_pages(SAMPLE_INDEX, "zebra")
    assert results == []


def test_find_empty_query():
    results = find_pages(SAMPLE_INDEX, "")
    assert results == []


def test_find_whitespace_query():
    results = find_pages(SAMPLE_INDEX, "   ")
    assert results == []


def test_find_case_insensitive():
    results = find_pages(SAMPLE_INDEX, "GOOD")
    assert len(results) > 0


def test_find_partial_match_returns_empty():
    # "good" is in index but "zebra" is not - should return empty
    results = find_pages(SAMPLE_INDEX, "good zebra")
    assert results == []


# ---------- print_index_entry() tests ----------

def test_print_word_not_in_index(capsys):
    print_index_entry(SAMPLE_INDEX, "zebra")
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_print_empty_word(capsys):
    print_index_entry(SAMPLE_INDEX, "")
    captured = capsys.readouterr()
    assert "provide a word" in captured.out


def test_print_valid_word(capsys):
    print_index_entry(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    assert "good" in captured.out
    assert "Frequency" in captured.out