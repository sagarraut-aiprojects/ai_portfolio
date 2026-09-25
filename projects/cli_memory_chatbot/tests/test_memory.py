import tempfile
from pathlib import Path
import json
import memory


def test_save_and_load_memory():
    messages = [
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hi!"
        }
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        memory.MEMORY_FILE = Path(temp_dir) / "test_memory.json"

        memory.save_memory(messages)

        loaded_messages = memory.load_memory()

        assert loaded_messages == messages


def test_load_memory_when_json_is_corrupted():
    with tempfile.TemporaryDirectory() as temp_dir:
        memory.MEMORY_FILE = Path(temp_dir) / "test_memory.json"

        memory.MEMORY_FILE.write_text(
            '{"role": "user"',
            encoding="utf-8"
        )

        loaded_messages = memory.load_memory()

        assert loaded_messages == []

def test_load_memory_when_file_does_not_exist():
    with tempfile.TemporaryDirectory() as temp_dir:
        memory.MEMORY_FILE = Path(temp_dir) / "does_not_exist.json"

        loaded_messages = memory.load_memory()

        assert loaded_messages == []

def test_save_memory_creates_file():
    messages = [
        {
            "role": "user",
            "content": "Test message"
        }
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        memory.MEMORY_FILE = Path(temp_dir) / "new_memory.json"

        memory.save_memory(messages)

        assert memory.MEMORY_FILE.exists()

def test_save_memory_writes_correct_json():
    messages = [
        {
            "role": "user",
            "content": "Hello"
        }
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        memory.MEMORY_FILE = Path(temp_dir) / "memory.json"

        memory.save_memory(messages)

        with open(memory.MEMORY_FILE, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        assert saved_data == messages