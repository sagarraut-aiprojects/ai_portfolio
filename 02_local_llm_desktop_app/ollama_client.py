from ollama import chat

MODEL = "phi3:latest"

def chat_with_model(messages):

    try:

        stream = chat(
            model=MODEL,
            messages=messages,
            stream=True
        )

        for chunk in stream:

            text = chunk.message.content

            yield text

    except Exception as e:

        error_message = str(e)

        if "connection" in error_message.lower():
            raise RuntimeError(
                "Unable to connect to Ollama.\n\n"
                "Please make sure Ollama is installed and running."
            )

        elif "not found" in error_message.lower():
            raise RuntimeError(
                "Phi-3 could not be found.\n\n"
                "Please make sure the Phi-3 model is installed."
            )

        else:
            raise RuntimeError(
                "Ollama encountered an unexpected error.\n\n"
                f"{error_message}"
            )

