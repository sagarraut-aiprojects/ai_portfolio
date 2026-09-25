from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai = OpenAI()


def getresponse(messages):
    response = openai.responses.create(
        model = "gpt-5.6-luna",
        input = messages
)

    return response.output_text

