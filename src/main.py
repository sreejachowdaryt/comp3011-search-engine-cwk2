# main.py - Command-line interface for the search engine

import json
import os
from src.crawler import crawl
from src.indexer import build_index, compute_tf_idf
from src.search import find_pages, print_index_entry

INDEX_PATH = "data/index.json"


def save_index(index):
    """Saves the index to a JSON file."""
    os.makedirs("data", exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print(f"Index saved to {INDEX_PATH}")


def load_index():
    """Loads the index from a JSON file."""
    if not os.path.exists(INDEX_PATH):
        print("No index found. Please run 'build' first.")
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)
    print(f"Index loaded from {INDEX_PATH} ({len(index)} words)")
    return index


def main():
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
            pages = crawl()
            index = build_index(pages)
            index = compute_tf_idf(index, pages)
            save_index(index)

        elif command == "load":
            index = load_index()

        elif command == "print":
            if index is None:
                print("No index loaded. Use 'build' or 'load' first.")
            elif len(parts) < 2:
                print("Usage: print <word>")
            else:
                print_index_entry(index, parts[1])

        elif command == "find":
            if index is None:
                print("No index loaded. Use 'build' or 'load' first.")
            elif len(parts) < 2:
                print("Usage: find <query>")
            else:
                query = " ".join(parts[1:])
                results = find_pages(index, query)
                if results:
                    print(f"\nFound {len(results)} page(s):")
                    for i, (url, score) in enumerate(results, 1):
                        print(f"  {i}. {url}  (score: {score})")
        else:
            print(f"Unknown command: '{command}'. Try: build | load | print | find | quit")


if __name__ == "__main__":
    main()