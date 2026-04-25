# search.py - Query processing and search logic

from src.indexer import tokenize
import difflib


def suggest_word(word: str, index: dict) -> str | None:
    """
    Suggests the closest matching word in the index.
    Used when a search term is not found.

    Args:
        word (str): The word that wasn't found
        index (dict): The inverted index to search against

    Returns:
        str | None: The closest match, or None if no good match found

    Time complexity:  O(v) where v = vocabulary size
    Space complexity: O(1)
    """
    matches = difflib.get_close_matches(word, index.keys(), n=1, cutoff=0.75)
    return matches[0] if matches else None


def suggest_related_words(query_words: list[str], index: dict, top_n: int = 5) -> list[str]:
    """
    Suggests related words using pointwise mutual information (PMI) style
    scoring. Words that co-occur with the query AND are specific to those
    pages (not universal) score highest.

    Score = (pages_with_word_on_matching / total_matching) 
            / (total_pages_with_word / total_pages)

    This rewards words that appear disproportionately often on matching
    pages compared to the rest of the index — the core idea behind PMI.

    Args:
        query_words (list): The words already in the query
        index (dict): The inverted index
        top_n (int): Number of related words to return

    Returns:
        list: Top related words sorted by PMI-style score

    Time complexity:  O(v * p) where v = vocabulary size,
                      p = average pages per word
    Space complexity: O(v) where v = vocabulary size
    """
    if not query_words:
        return []

    # Get pages matching ALL query words
    matching_pages = None
    for word in query_words:
        if word not in index:
            return []
        pages = set(index[word].keys())
        if matching_pages is None:
            matching_pages = pages
        else:
            matching_pages = matching_pages & pages

    if not matching_pages:
        return []

    total_matching = len(matching_pages)
    total_pages = len(index[query_words[0]])  # approximate total pages

    # Get a better total pages count from the largest word
    total_pages = max(len(page_data) for page_data in index.values())

    related_scores: dict[str, float] = {}

    for word, page_data in index.items():
        if word in query_words:
            continue

        # How many matching pages does this word appear on?
        overlap = [url for url in matching_pages if url in page_data]
        if not overlap:
            continue

        # P(word | matching pages) — how common is word on matching pages
        p_word_given_match = len(overlap) / total_matching

        # P(word) — how common is word across ALL pages
        p_word = len(page_data) / total_pages

        # PMI-style score: if word appears more on matching pages than
        # expected by chance, it's genuinely related
        if p_word > 0:
            pmi_score = p_word_given_match / p_word
            # Only suggest words that appear on at least 10% of matching pages
            if p_word_given_match >= 0.2:
                related_scores[word] = pmi_score

    sorted_related = sorted(related_scores.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_related[:top_n]]


def find_pages(index: dict, query: str) -> list[tuple[str, float]]:
    """
    Finds all pages containing ALL words in the query.
    Results are ranked by combined TF-IDF score.
    Suggests corrections for ALL misspelled words before returning.
    Also displays related terms based on co-occurrence.

    Args:
        index (dict): The inverted index
        query (str): One or more search terms e.g. "good friends"

    Returns:
        list: Sorted list of (url, score) tuples, best match first

    Time complexity:  O(q * p) where q = number of query words,
                      p = average number of pages per word
    Space complexity: O(p) for storing matching URL sets
    """
    if not query or not query.strip():
        print("Please enter a search term.")
        return []

    words = tokenize(query)

    if not words:
        print("No valid search terms found.")
        return []

    # Check ALL words first and collect suggestions for any missing ones
    missing = []
    for word in words:
        if word not in index:
            suggestion = suggest_word(word, index)
            if suggestion:
                missing.append(f"'{word}' not found in index. Did you mean '{suggestion}'?")
            else:
                missing.append(f"'{word}' not found in index.")

    if missing:
        for msg in missing:
            print(msg)
        return []

    # Get pages that contain ALL query words (AND logic)
    matching_urls = None
    for word in words:
        pages_with_word = set(index[word].keys())
        if matching_urls is None:
            matching_urls = pages_with_word
        else:
            matching_urls = matching_urls & pages_with_word

    if not matching_urls:
        print("No pages found containing all search terms.")
        return []

    # Rank by combined TF-IDF score
    results = []
    for url in matching_urls:
        score = sum(
            index[word][url].get("tf_idf", 0)
            for word in words
            if url in index[word]
        )
        results.append((url, round(score, 6)))

    results.sort(key=lambda x: x[1], reverse=True)

    # Show related word suggestions
    related = suggest_related_words(words, index)
    if related:
        print(f"  Related terms: {', '.join(related)}")

    return results


def print_index_entry(index: dict, word: str) -> None:
    """
    Prints the inverted index entry for a given word.

    Args:
        index (dict): The inverted index
        word (str): The word to look up

    Time complexity:  O(p) where p = number of pages containing the word
    Space complexity: O(1) — prints directly, no additional storage
    """
    word = word.lower().strip()

    if not word:
        print("Please provide a word to print.")
        return

    if word not in index:
        suggestion = suggest_word(word, index)
        if suggestion:
            print(f"'{word}' not found in index. Did you mean '{suggestion}'?")
        else:
            print(f"'{word}' not found in index.")
        return

    print(f"\nIndex entry for '{word}':")
    print("-" * 40)
    for url, stats in index[word].items():
        print(f"  URL: {url}")
        print(f"    Frequency : {stats['frequency']}")
        print(f"    Positions : {stats['positions']}")
        print(f"    TF-IDF    : {stats.get('tf_idf', 'N/A')}")
    print("-" * 40)