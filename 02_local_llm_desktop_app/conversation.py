import json
from pathlib import Path
from datetime import datetime
import uuid


# Folder where conversations will be stored
CONVERSATIONS_DIR = (Path.home() / "AppData" / "Local" / "ProfSagarLocalAI" / "conversations")


def create_conversation():
    """Create a new empty conversation."""

    conversation = {
        "id": str(uuid.uuid4()),
        "title": "New Chat",
        "created_at": datetime.now().isoformat(),
        "messages": []
    }

    return conversation


def save_conversation(conversation):
    """Save a conversation to a JSON file."""

    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = CONVERSATIONS_DIR / f"{conversation['id']}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            conversation,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_conversation(conversation_id):
    """Load a conversation from a JSON file."""

    file_path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_all_conversations():
    """Load all saved conversations."""

    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)

    conversations = []

    for file_path in CONVERSATIONS_DIR.glob("*.json"):

        with open(file_path, "r", encoding="utf-8") as file:
            conversation = json.load(file)

        conversations.append(conversation)

    conversations.sort(
        key=lambda conversation: conversation["created_at"],
        reverse=True
    )

    return conversations


def delete_conversation(conversation_id):
    """Delete a saved conversation."""

    file_path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    if file_path.exists():
        file_path.unlink()