import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

MODEL_NAME = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna",
)


def generate_segment_insights(segment_summary):
    """
    Generate business insights from RFM segment summaries.

    The LLM receives pre-calculated statistics.
    It does not perform the underlying RFM calculations.
    """

    client = OpenAI()

    summary_text = segment_summary.to_string(
        index=False
    )

    prompt = f"""
You are a customer analytics consultant.

Analyze the following RFM customer segmentation results.

The statistics have already been calculated using Python.
Do not recalculate them.

RFM SEGMENT SUMMARY:

{summary_text}

Provide a concise business analysis covering:

1. The characteristics of each customer segment.
2. Important differences between the segments.
3. Potential customer-retention or engagement strategies
   for each segment.
4. Which segments deserve management attention and why,
   based only on the provided data.
5. Three key business insights from the analysis.

Clearly distinguish observed data from suggested business actions.
Do not invent information that is not present in the data.
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text