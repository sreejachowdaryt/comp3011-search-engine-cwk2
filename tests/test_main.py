# tests for main.py

import pytest
import json
import os
from unittest.mock import patch, MagicMock
from src.main import save_index, load_index
from src.main import main


SAMPLE_INDEX = {
    "hello": {
        "https://example.com": {
            "frequency": 1,
            "positions": [0],
            "tf_idf": 0.5
        }
    }
}


def test_save_index_creates_file(tmp_path):
    filepath = str(tmp_path / "index.json")
    with patch("src.main.INDEX_PATH", filepath):
        save_index(SAMPLE_INDEX)
    assert os.path.exists(filepath)


def test_save_index_correct_content(tmp_path):
    filepath = str(tmp_path / "index.json")
    with patch("src.main.INDEX_PATH", filepath):
        save_index(SAMPLE_INDEX)
    with open(filepath, "r") as f:
        loaded = json.load(f)
    assert loaded == SAMPLE_INDEX


def test_load_index_returns_data(tmp_path):
    filepath = str(tmp_path / "index.json")
    with open(filepath, "w") as f:
        json.dump(SAMPLE_INDEX, f)
    with patch("src.main.INDEX_PATH", filepath):
        result = load_index()
    assert result == SAMPLE_INDEX


def test_load_index_missing_file(tmp_path):
    filepath = str(tmp_path / "nonexistent.json")
    with patch("src.main.INDEX_PATH", filepath):
        result = load_index()
    assert result is None


def test_load_index_word_count(tmp_path):
    filepath = str(tmp_path / "index.json")
    with open(filepath, "w") as f:
        json.dump(SAMPLE_INDEX, f)
    with patch("src.main.INDEX_PATH", filepath):
        result = load_index()
    assert len(result) == 1


def test_save_creates_data_directory(tmp_path):
    filepath = str(tmp_path / "subdir" / "index.json")
    with patch("src.main.INDEX_PATH", filepath):
        with patch("src.main.os.makedirs") as mock_makedirs:
            with patch("builtins.open", MagicMock()):
                with patch("json.dump"):
                    save_index(SAMPLE_INDEX)
    mock_makedirs.assert_called_once()

def test_main_quit_command():
    with patch("builtins.input", return_value="quit"):
        main()  # Should exit cleanly without error


def test_main_empty_input():
    inputs = iter(["", "quit"])
    with patch("builtins.input", side_effect=inputs):
        main()


def test_main_load_no_index(tmp_path):
    filepath = str(tmp_path / "nonexistent.json")
    inputs = iter(["load", "quit"])
    with patch("builtins.input", side_effect=inputs):
        with patch("src.main.INDEX_PATH", filepath):
            main()


def test_main_print_no_index_loaded():
    inputs = iter(["print hello", "quit"])
    with patch("builtins.input", side_effect=inputs):
        main()


def test_main_find_no_index_loaded():
    inputs = iter(["find love", "quit"])
    with patch("builtins.input", side_effect=inputs):
        main()


def test_main_unknown_command():
    inputs = iter(["invalidcommand", "quit"])
    with patch("builtins.input", side_effect=inputs):
        main()


def test_main_print_with_index(tmp_path):
    filepath = str(tmp_path / "index.json")
    with open(filepath, "w") as f:
        json.dump(SAMPLE_INDEX, f)
    inputs = iter(["load", "print hello", "quit"])
    with patch("builtins.input", side_effect=inputs):
        with patch("src.main.INDEX_PATH", filepath):
            main()


def test_main_find_with_index(tmp_path):
    filepath = str(tmp_path / "index.json")
    with open(filepath, "w") as f:
        json.dump(SAMPLE_INDEX, f)
    inputs = iter(["load", "find hello", "quit"])
    with patch("builtins.input", side_effect=inputs):
        with patch("src.main.INDEX_PATH", filepath):
            main()


def test_main_print_missing_word_argument(tmp_path):
    filepath = str(tmp_path / "index.json")
    with open(filepath, "w") as f:
        json.dump(SAMPLE_INDEX, f)
    inputs = iter(["load", "print", "quit"])
    with patch("builtins.input", side_effect=inputs):
        with patch("src.main.INDEX_PATH", filepath):
            main()


def test_main_find_missing_query_argument(tmp_path):
    filepath = str(tmp_path / "index.json")
    with open(filepath, "w") as f:
        json.dump(SAMPLE_INDEX, f)
    inputs = iter(["load", "find", "quit"])
    with patch("builtins.input", side_effect=inputs):
        with patch("src.main.INDEX_PATH", filepath):
            main()


def test_main_keyboard_interrupt():
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        main()  # Should handle gracefully