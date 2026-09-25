# CLI Memory Chatbot

A command-line AI chatbot built with Python and the OpenAI API, featuring both in-session and persistent conversation memory.

## Project Overview

This project demonstrates how to build a simple but structured AI application from the ground up.

The chatbot:

* Accepts user input through the command line
* Sends conversations to an LLM
* Maintains conversation context during the session
* Persists conversation history to a JSON file
* Restores previous conversations when restarted
* Handles API failures gracefully
* Validates empty user input
* Handles corrupted memory files
* Includes automated tests using `pytest`

## Architecture

```text
User
 │
 ▼
main.py
 │
 ▼
cli_memory_chatbot.py
 │
 ├──► memory.py ──► memory.json
 │
 └──► llm.py ──► OpenAI API
          │
          ▼
       config.py
```

### Files

| File                    | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| `main.py`               | Application entry point                        |
| `cli_memory_chatbot.py` | Main chatbot logic                             |
| `llm.py`                | Handles communication with the OpenAI API      |
| `memory.py`             | Loads and saves persistent conversation memory |
| `config.py`             | Stores application configuration               |
| `memory.json`           | Persistent conversation history                |
| `tests/test_memory.py`  | Tests memory functionality                     |
| `tests/test_chatbot.py` | Tests chatbot behavior                         |

## Technologies Used

* Python
* OpenAI API
* OpenAI Python SDK
* python-dotenv
* JSON
* pytest
* uv

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sagarraut-aiprojects/ai_portfolio.git
cd ai_portfolio/projects/cli_memory_chatbot
```

### 2. Create the environment

```bash
uv sync
```

### 3. Configure the API key

Create a `.env` file in the project directory:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git through `.gitignore`.

### 4. Run the chatbot

```bash
uv run python src/main.py
```

You should see:

```text
CLI memory ChatBot
Type 'exit' to quit.
```

Type `exit` to end the conversation.

## Running the Tests

Run the complete test suite with:

```bash
uv run pytest
```

The project currently contains **9 automated tests** covering:

* Saving and loading memory
* Corrupted JSON handling
* Missing memory files
* Memory file creation
* Correct JSON persistence
* Successful chatbot responses
* API failure handling
* Empty input validation
* Conversation persistence

## Persistent Memory

Conversation history is stored in:

```text
memory.json
```

When the chatbot starts, it loads the previous conversation:

```python
messages = load_memory()
```

New user and assistant messages are appended to the conversation and saved after each successful response.

This allows the chatbot to maintain context even after the application is restarted.

## Error Handling

The application handles several failure scenarios.

### API failure

If the API request fails, the chatbot catches the exception and continues running rather than terminating.

### Empty input

Blank or whitespace-only input is rejected:

```text
Please enter a message.
```

### Corrupted memory

If `memory.json` contains invalid JSON, the application starts with an empty conversation instead of crashing.

## Design Decisions

### Why JSON?

JSON was chosen because it is simple, human-readable, requires no database server, and is appropriate for a small demonstration application.

### Why separate the LLM and memory logic?

The application separates responsibilities:

```text
LLM communication → llm.py
Memory management → memory.py
Chatbot workflow  → cli_memory_chatbot.py
Configuration     → config.py
```

This makes the application easier to test, maintain, and extend.

### Why mock the API in tests?

The automated tests do not make real API calls.

Instead, the OpenAI response is replaced with a controlled test response. This makes the tests:

* Faster
* Cheaper
* Deterministic
* Independent of network availability

## Current Limitations

This is intentionally a small first-generation memory chatbot.

The current implementation:

* Stores all conversation history in a single JSON file
* Sends the complete conversation history to the model
* Does not use a database
* Does not summarize older conversations
* Does not implement semantic memory
* Does not have a graphical interface
* Does not implement authentication or multiple users

These limitations are deliberate and provide a foundation for more advanced projects in the portfolio.

## Learning Outcomes

This project demonstrates practical understanding of:

* Python application structure
* API integration
* Environment variables
* Conversation state
* Persistent storage
* Exception handling
* Input validation
* Unit testing
* Mocking external services
* Separation of responsibilities
* Git/GitHub project organization

## Portfolio Progression

This project represents the foundation for the subsequent AI projects in the portfolio.

The progression moves from:

```text
API Calls
   ↓
Conversation State
   ↓
Persistent Memory
   ↓
Testing & Error Handling
   ↓
RAG
   ↓
Tool Calling
   ↓
Agents
   ↓
Production AI Applications
```
