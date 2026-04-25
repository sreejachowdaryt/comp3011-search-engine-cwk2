# tests for search.py

import pytest
from src.search import find_pages, print_index_entry, suggest_word, suggest_related_words


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


# ---------- suggest_related_words() tests ----------

def test_related_words_returns_list():
    related = suggest_related_words(["good"], SAMPLE_INDEX)
    assert isinstance(related, list)


def test_related_words_excludes_query_words():
    related = suggest_related_words(["good"], SAMPLE_INDEX)
    assert "good" not in related


def test_related_words_empty_query():
    related = suggest_related_words([], SAMPLE_INDEX)
    assert related == []


def test_related_words_unknown_word():
    related = suggest_related_words(["zebra"], SAMPLE_INDEX)
    assert related == []


def test_related_words_returns_cooccurring_words():
    # "good" and "friends" both appear on page1
    # so searching "good" should suggest "friends" as related
    related = suggest_related_words(["good"], SAMPLE_INDEX)
    assert "friends" in related


def test_related_words_respects_top_n():
    related = suggest_related_words(["good"], SAMPLE_INDEX, top_n=1)
    assert len(related) <= 1


def test_related_words_multi_word_query():
    # searching for both "good" and "friends" together
    # should return empty since they only share page1
    # and no other word appears on page1
    related = suggest_related_words(["good", "friends"], SAMPLE_INDEX)
    assert isinstance(related, list)


def test_related_words_no_matching_pages():
    # "good" is on page1/page2, "indifference" is on page3
    # no overlap so no related words
    related = suggest_related_words(["good", "indifference"], SAMPLE_INDEX)
    assert related == []


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


def test_find_shows_related_terms(capsys):
    # "good" appears on page1 and page2
    # "friends" also appears on page1 so should be suggested as related
    results = find_pages(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    assert "Related terms" in captured.out


def test_find_related_excludes_query_word(capsys):
    # "good" should not appear in its own related terms
    results = find_pages(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    if "Related terms" in captured.out:
        assert "good" not in captured.out.split("Related terms:")[1].split("\n")[0]


def test_find_returns_list_of_tuples():
    results = find_pages(SAMPLE_INDEX, "good")
    assert all(isinstance(r, tuple) for r in results)
    assert all(len(r) == 2 for r in results)


def test_find_scores_are_floats():
    results = find_pages(SAMPLE_INDEX, "good")
    assert all(isinstance(score, float) for _, score in results)


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


def test_print_shows_tfidf(capsys):
    print_index_entry(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    assert "TF-IDF" in captured.out


def test_print_shows_positions(capsys):
    print_index_entry(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    assert "Positions" in captured.out


def test_print_case_insensitive(capsys):
    print_index_entry(SAMPLE_INDEX, "GOOD")
    captured = capsys.readouterr()
    assert "good" in captured.out
    assert "Frequency" in captured.out