# main.py - Command-line interface for the search engine

import json
import os
import time
from src.crawler import crawl
from src.indexer import build_index, compute_tf_idf
from src.search import find_pages, print_index_entry

INDEX_PATH = "data/index.json"


def save_index(index: dict) -> None:
    """
    Saves the index to a JSON file.

    Args:
        index (dict): The inverted index to save

    Time complexity:  O(n) where n = total entries in index
    Space complexity: O(1) additional space
    """
    os.makedirs("data", exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print(f"Index saved to {INDEX_PATH}")


def load_index() -> dict | None:
    """
    Loads the index from a JSON file.

    Returns:
        dict | None: The loaded index, or None if file not found

    Time complexity:  O(n) where n = total entries in index
    Space complexity: O(n) to load index into memory
    """
    if not os.path.exists(INDEX_PATH):
        print("No index found. Please run 'build' first.")
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)
    print(f"Index loaded from {INDEX_PATH} ({len(index)} words)")
    return index


def main() -> None:
    """
    Runs the interactive command-line search engine shell.
    Accepts commands: build, load, print, find, quit.
    All search operations are benchmarked and display query time.
    """
    index = None
    print("Search Engine ready. Commands: build | load | print <word> | find <query> | quit")
    print("-" * 60)

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()

        if command == "quit":
            print("Goodbye!")
            break

        elif command == "build":
            print("Building index - this will take several minutes due to politeness window...")
            start = time.time()
            pages = crawl()
            index = build_index(pages)
            index = compute_tf_idf(index, pages)
            save_index(index)
            elapsed = time.time() - start
            print(f"Build completed in {elapsed:.2f}s")

        elif command == "load":
            start = time.time()
            index = load_index()
            elapsed = time.time() - start
            if index is not None:
                print(f"Load completed in {elapsed:.4f}s")

        elif command == "print":
            if index is None:
                print("No index loaded. Use 'build' or 'load' first.")
            elif len(parts) < 2:
                print("Usage: print <word> [word2] [word3]...")
            else:
                start = time.time()
                for word in parts[1:]:
                    print_index_entry(index, word)
                elapsed = time.time() - start
                print(f"  Query completed in {elapsed:.4f}s")

        elif command == "find":
            if index is None:
                print("No index loaded. Use 'build' or 'load' first.")
            elif len(parts) < 2:
                print("Usage: find <query>")
            else:
                query = " ".join(parts[1:])
                start = time.time()
                results = find_pages(index, query)
                elapsed = time.time() - start
                if results:
                    print(f"\nFound {len(results)} page(s) in {elapsed:.4f}s:")
                    for i, (url, score) in enumerate(results, 1):
                        print(f"  {i}. {url}  (score: {score})")
                else:
                    print(f"  Query completed in {elapsed:.4f}s")

        else:
            print(f"Unknown command: '{command}'. Try: build | load | print | find | quit")


if __name__ == "__main__":
    main()