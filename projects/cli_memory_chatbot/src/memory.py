import json
from pathlib import Path


MEMORY_FILE = Path(__file__).parent.parent / "memory.json"


def load_memory():
    if not MEMORY_FILE.exists():
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)

    except json.JSONDecodeError:
         print("Warning! memory.json is corrupted. Starting with empty memory.")
         return []
        


def save_memory(messages):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)