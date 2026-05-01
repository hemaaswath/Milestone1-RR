from __future__ import annotations

import os
from dotenv import load_dotenv

from groq import Groq

# Load environment variables from .env file
load_dotenv()


DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"


def run_groq_inference(prompt: str, model: str = DEFAULT_GROQ_MODEL) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON generator for restaurant ranking.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or "{}"

