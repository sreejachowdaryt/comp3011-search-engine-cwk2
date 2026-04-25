# indexer.py - Builds the inverted index from crawled pages

import re
import math
from collections import defaultdict


def tokenize(text: str) -> list[str]:
    """
    Converts raw page text into a list of clean, lowercase tokens.
    Strips punctuation and normalises whitespace.
    
    Args:
        text (str): Raw text from a crawled page
        
    Returns:
        list: Clean lowercase words
    """
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    return words


def build_index(pages: dict[str, str]) -> dict:
    """
    Builds an inverted index from a dictionary of crawled pages.
    
    Stores for each word:
        - frequency: how many times it appears in that page
        - positions: list of word positions it appears at
    
    Args:
        pages (dict): {url: text_content} from the crawler
        
    Returns:
        dict: Inverted index in the format:
              {word: {url: {frequency: int, positions: [int]}}}
    
    Time complexity:  O(n * w) where n = number of pages,
                      w = average words per page

    Space complexity: O(v * p) where v = vocabulary size,
                      p = number of pages
    """
    index = defaultdict(dict)

    for url, text in pages.items():
        tokens = tokenize(text)

        for position, word in enumerate(tokens):
            if url not in index[word]:
                index[word][url] = {
                    "frequency": 0,
                    "positions": []
                }
            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)

    print(f"Index built with {len(index)} unique words.")
    return dict(index)


def compute_tf_idf(index: dict, pages: dict[str, str]) -> dict:
    """
    Adds TF-IDF score to each word/page entry in the index.
    Used to rank search results by relevance.
    
    TF  = frequency of word in page / total words in page
    IDF = log(total pages / pages containing word)
    
    Args:
        index (dict): The inverted index from build_index()
        pages (dict): {url: text_content} from the crawler
        
    Returns:
        dict: Index with tf_idf scores added to each entry
    
    Time complexity:  O(v * p) where v = vocabulary size,
                      p = average pages per word

    Space complexity: O(n) where n = number of pages, for word count cache
    """

    total_pages = len(pages)
    page_word_counts = {}

    for url, text in pages.items():
        page_word_counts[url] = len(tokenize(text))

    for word, url_data in index.items():
        pages_with_word = len(url_data)
        idf = math.log(total_pages / (1 + pages_with_word))

        for url, stats in url_data.items():
            total_words = page_word_counts.get(url, 1)
            tf = stats["frequency"] / total_words
            stats["tf_idf"] = round(tf * idf, 6)

    return index