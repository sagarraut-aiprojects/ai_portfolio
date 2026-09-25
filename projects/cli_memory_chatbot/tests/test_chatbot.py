from unittest.mock import patch

import cli_memory_chatbot


def test_chatbot_gets_response():
    fake_response = "Hello! This is a test response."

    with patch(
        "cli_memory_chatbot.getresponse",
        return_value=fake_response
    ):
        with patch(
            "builtins.input",
            side_effect=["Hello", "exit"]
        ):
            with patch("builtins.print") as mock_print:
                cli_memory_chatbot.run_chatbot()

    mock_print.assert_any_call(
        "Assistant",
        fake_response
    )

def test_chatbot_handles_api_failure():
    with patch(
        "cli_memory_chatbot.getresponse",
        return_value=None
    ):
        with patch(
            "builtins.input",
            side_effect=["Hello", "exit"]
        ):
            cli_memory_chatbot.run_chatbot()    

def test_chatbot_rejects_empty_input():
    with patch(
        "builtins.input",
        side_effect=["", "exit"]
    ):
        with patch("builtins.print") as mock_print:
            cli_memory_chatbot.run_chatbot()

    mock_print.assert_any_call(
        "Please enter a message."
    )

def test_chatbot_saves_conversation():
    fake_response = "Hello! This is a test response."

    with patch(
        "cli_memory_chatbot.load_memory",
        return_value=[]
    ):
        with patch(
            "cli_memory_chatbot.save_memory"
        ) as mock_save_memory:
            with patch(
                "cli_memory_chatbot.getresponse",
                return_value=fake_response
            ):
                with patch(
                    "builtins.input",
                    side_effect=["Hello", "exit"]
                ):
                    cli_memory_chatbot.run_chatbot()

    mock_save_memory.assert_called_once_with([
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": fake_response
        }
    ])