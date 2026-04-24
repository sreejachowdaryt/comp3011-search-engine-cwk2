# tests for indexer.py

import pytest
from src.indexer import tokenize, build_index, compute_tf_idf


# ---------- tokenize() tests ----------

def test_tokenize_lowercase():
    tokens = tokenize("Hello World")
    assert tokens == ["hello", "world"]


def test_tokenize_strips_punctuation():
    tokens = tokenize("don't stop, believing!")
    assert "don" in tokens
    assert "stop" in tokens
    assert "believing" in tokens


def test_tokenize_empty_string():
    tokens = tokenize("")
    assert tokens == []


def test_tokenize_numbers_excluded():
    tokens = tokenize("page 42 has content")
    assert "42" not in tokens
    assert "page" in tokens


# ---------- build_index() tests ----------

SAMPLE_PAGES = {
    "https://example.com/page1": "the cat sat on the mat",
    "https://example.com/page2": "the dog sat on the log",
}


def test_index_contains_word():
    index = build_index(SAMPLE_PAGES)
    assert "cat" in index


def test_index_correct_frequency():
    index = build_index(SAMPLE_PAGES)
    # "the" appears twice in page1
    assert index["the"]["https://example.com/page1"]["frequency"] == 2


def test_index_correct_positions():
    index = build_index(SAMPLE_PAGES)
    # "cat" is at position 1 in page1
    assert 1 in index["cat"]["https://example.com/page1"]["positions"]


def test_index_word_in_multiple_pages():
    index = build_index(SAMPLE_PAGES)
    # "sat" appears in both pages
    assert "https://example.com/page1" in index["sat"]
    assert "https://example.com/page2" in index["sat"]


def test_index_case_insensitive():
    pages = {"https://example.com/": "Good good GOOD"}
    index = build_index(pages)
    assert index["good"]["https://example.com/"]["frequency"] == 3


def test_index_empty_pages():
    index = build_index({})
    assert index == {}


def test_index_missing_word():
    index = build_index(SAMPLE_PAGES)
    assert "zebra" not in index


# ---------- compute_tf_idf() tests ----------

def test_tfidf_adds_scores():
    index = build_index(SAMPLE_PAGES)
    index = compute_tf_idf(index, SAMPLE_PAGES)
    assert "tf_idf" in index["cat"]["https://example.com/page1"]


def test_tfidf_unique_word_scores_higher():
    index = build_index(SAMPLE_PAGES)
    index = compute_tf_idf(index, SAMPLE_PAGES)
    # "cat" only in page1, "the" in both - cat should have higher idf
    cat_score = index["cat"]["https://example.com/page1"]["tf_idf"]
    the_score = index["the"]["https://example.com/page1"]["tf_idf"]
    assert cat_score > the_score