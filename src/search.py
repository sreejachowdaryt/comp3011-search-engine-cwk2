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


def find_pages(index: dict, query: str) -> list[tuple[str, float]]:
    """
    Finds all pages containing ALL words in the query.
    Results are ranked by combined TF-IDF score.

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

    # Get pages that contain ALL query words (AND logic)
    matching_urls = None

    for word in words:
        if word not in index:
            suggestion = suggest_word(word, index)
            if suggestion:
                print(f"'{word}' not found in index. Did you mean '{suggestion}'?")
            else:
                print(f"'{word}' not found in index.")
            return []
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