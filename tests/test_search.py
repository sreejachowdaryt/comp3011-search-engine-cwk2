# tests for search.py

import pytest
from src.search import find_pages, print_index_entry, suggest_word


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


# ---------- suggest_word() tests ----------

def test_suggest_word_finds_close_match():
    index = {"friends": {}, "freedom": {}, "french": {}}
    suggestion = suggest_word("freinds", index)
    assert suggestion == "friends"


def test_suggest_word_no_match():
    index = {"friends": {}, "freedom": {}}
    suggestion = suggest_word("xyzqwerty", index)
    assert suggestion is None


def test_suggest_word_exact_match():
    index = {"friends": {}, "freedom": {}}
    suggestion = suggest_word("friends", index)
    assert suggestion == "friends"


# ---------- find_pages() tests ----------

def test_find_single_word():
    results = find_pages(SAMPLE_INDEX, "indifference")
    urls = [r[0] for r in results]
    assert "https://example.com/page3" in urls


def test_find_multi_word():
    results = find_pages(SAMPLE_INDEX, "good friends")
    urls = [r[0] for r in results]
    assert "https://example.com/page1" in urls
    assert "https://example.com/page2" not in urls


def test_find_returns_ranked_results():
    results = find_pages(SAMPLE_INDEX, "good")
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
    results = find_pages(SAMPLE_INDEX, "good zebra")
    assert results == []


def test_find_suggests_correction(capsys):
    results = find_pages(SAMPLE_INDEX, "freinds")
    captured = capsys.readouterr()
    assert "Did you mean" in captured.out


def test_find_no_suggestion_for_gibberish(capsys):
    results = find_pages(SAMPLE_INDEX, "xyzqwerty")
    captured = capsys.readouterr()
    assert "not found in index" in captured.out
    assert "Did you mean" not in captured.out


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

def test_print_suggests_correction(capsys):
    print_index_entry(SAMPLE_INDEX, "freinds")
    captured = capsys.readouterr()
    assert "Did you mean" in captured.out