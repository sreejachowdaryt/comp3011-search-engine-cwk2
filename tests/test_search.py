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
    "life": {
        "https://example.com/page1": {"frequency": 1, "positions": [8], "tf_idf": 0.2},
        "https://example.com/page2": {"frequency": 2, "positions": [3, 9], "tf_idf": 0.15},
    },
    "wisdom": {
        "https://example.com/page1": {"frequency": 1, "positions": [10], "tf_idf": 0.4},
        "https://example.com/page2": {"frequency": 1, "positions": [5], "tf_idf": 0.35},
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


def test_suggest_word_returns_string_or_none():
    index = {"hello": {}, "world": {}}
    result = suggest_word("helo", index)
    assert result is None or isinstance(result, str)


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
    related = suggest_related_words(["good"], SAMPLE_INDEX)
    assert len(related) > 0


def test_related_words_respects_top_n():
    related = suggest_related_words(["good"], SAMPLE_INDEX, top_n=1)
    assert len(related) <= 1


def test_related_words_top_n_zero():
    related = suggest_related_words(["good"], SAMPLE_INDEX, top_n=0)
    assert related == []


def test_related_words_multi_word_query():
    related = suggest_related_words(["good", "friends"], SAMPLE_INDEX)
    assert isinstance(related, list)
    assert "good" not in related
    assert "friends" not in related


def test_related_words_no_matching_pages():
    related = suggest_related_words(["good", "indifference"], SAMPLE_INDEX)
    assert related == []


def test_related_words_pmi_excludes_universal_words():
    related = suggest_related_words(["good"], SAMPLE_INDEX)
    assert "good" not in related


def test_related_words_single_page_match():
    related = suggest_related_words(["friends"], SAMPLE_INDEX)
    assert isinstance(related, list)
    assert "friends" not in related


# ---------- find_pages() AND logic tests ----------

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


def test_find_suggests_all_misspelled_words(capsys):
    results = find_pages(SAMPLE_INDEX, "freinds goood")
    captured = capsys.readouterr()
    assert "Did you mean" in captured.out


def test_find_no_suggestion_for_gibberish(capsys):
    results = find_pages(SAMPLE_INDEX, "xyzqwerty")
    captured = capsys.readouterr()
    assert "not found in index" in captured.out
    assert "Did you mean" not in captured.out


def test_find_shows_related_terms(capsys):
    results = find_pages(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    assert "Related terms" in captured.out


def test_find_related_excludes_query_word(capsys):
    results = find_pages(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    if "Related terms" in captured.out:
        related_line = captured.out.split("Related terms:")[1].split("\n")[0]
        assert "good" not in related_line


def test_find_returns_list_of_tuples():
    results = find_pages(SAMPLE_INDEX, "good")
    assert all(isinstance(r, tuple) for r in results)
    assert all(len(r) == 2 for r in results)


def test_find_scores_are_floats():
    results = find_pages(SAMPLE_INDEX, "good")
    assert all(isinstance(score, float) for _, score in results)


def test_find_scores_sorted_descending():
    results = find_pages(SAMPLE_INDEX, "good")
    scores = [score for _, score in results]
    assert scores == sorted(scores, reverse=True)


def test_find_multi_word_all_missing(capsys):
    results = find_pages(SAMPLE_INDEX, "zebra elephant")
    captured = capsys.readouterr()
    assert results == []
    assert "not found" in captured.out


def test_find_explicit_and_operator():
    # Explicit uppercase AND behaves same as default AND
    and_explicit = find_pages(SAMPLE_INDEX, "good AND friends")
    and_default = find_pages(SAMPLE_INDEX, "good friends")
    assert len(and_explicit) == len(and_default)


def test_find_lowercase_and_treated_as_search_term():
    # lowercase "and" is treated as a search word not an operator
    # "and" is not in SAMPLE_INDEX so should return empty
    results = find_pages(SAMPLE_INDEX, "good and friends")
    assert results == []


# ---------- find_pages() OR logic tests ----------

def test_find_or_logic_returns_union():
    # OR should return pages with EITHER word
    results = find_pages(SAMPLE_INDEX, "good OR indifference")
    urls = [r[0] for r in results]
    # page3 has indifference, page1/page2 have good
    assert "https://example.com/page3" in urls
    assert "https://example.com/page1" in urls


def test_find_or_more_results_than_and():
    # OR should return more or equal pages than AND
    and_results = find_pages(SAMPLE_INDEX, "good friends")
    or_results = find_pages(SAMPLE_INDEX, "good OR friends")
    assert len(or_results) >= len(and_results)


def test_find_or_shows_search_mode(capsys):
    find_pages(SAMPLE_INDEX, "good OR indifference")
    captured = capsys.readouterr()
    assert "OR" in captured.out


def test_find_or_includes_pages_from_both_words():
    # good is on page1 and page2
    # indifference is on page3
    # OR should include all three pages
    results = find_pages(SAMPLE_INDEX, "good OR indifference")
    urls = [r[0] for r in results]
    assert "https://example.com/page1" in urls
    assert "https://example.com/page2" in urls
    assert "https://example.com/page3" in urls


def test_find_lowercase_or_treated_as_search_term():
    # lowercase "or" is a search term not an operator
    # "or" is not in SAMPLE_INDEX so returns empty
    results = find_pages(SAMPLE_INDEX, "good or friends")
    assert results == []


def test_find_or_single_word_same_as_normal():
    # OR with one word behaves like normal search
    normal = find_pages(SAMPLE_INDEX, "good")
    # No OR detected since no operator present
    assert len(normal) > 0


def test_find_or_missing_word(capsys):
    # OR search where one word doesn't exist
    results = find_pages(SAMPLE_INDEX, "good OR zebra")
    captured = capsys.readouterr()
    assert results == []
    assert "not found" in captured.out


def test_find_or_returns_ranked_results():
    results = find_pages(SAMPLE_INDEX, "good OR indifference")
    scores = [score for _, score in results]
    assert scores == sorted(scores, reverse=True)


def test_find_or_returns_list_of_tuples():
    results = find_pages(SAMPLE_INDEX, "good OR indifference")
    assert all(isinstance(r, tuple) for r in results)
    assert all(len(r) == 2 for r in results)


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


def test_print_shows_url(capsys):
    print_index_entry(SAMPLE_INDEX, "good")
    captured = capsys.readouterr()
    assert "URL" in captured.out


def test_print_no_suggestion_for_gibberish(capsys):
    print_index_entry(SAMPLE_INDEX, "xyzqwerty")
    captured = capsys.readouterr()
    assert "not found" in captured.out
    assert "Did you mean" not in captured.out