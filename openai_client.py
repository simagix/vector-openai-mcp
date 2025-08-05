"""
openai_client.py
@ken.chen

Provides a unified client for querying OpenAI or Azure OpenAI models.
Handles environment configuration, prompt building, and chat completion requests.

Usage:
    # Example usage in your own script:
    from openai_client import OpenAIClient
    client = OpenAIClient()
    response = client.get_response([{"role": "user", "content": "Hello"}])
"""

import os
import dotenv
import argparse
from openai import OpenAI
from openai.lib.azure import AzureOpenAI
from typing import List

class OpenAIClient:
    def __init__(self, model: str = None):
        self.use_azure = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
        self.model = model or ("gpt-35-turbo" if self.use_azure else "gpt-4o")
        if self.use_azure:
            if not os.getenv("AZURE_OPENAI_ENDPOINT") or not os.getenv("AZURE_OPENAI_API_KEY"):
                raise ValueError("Environment variables AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set.")
            self.client = AzureOpenAI(
                api_version="2024-12-01-preview",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            )
        else:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("Environment variable OPENAI_API_KEY must be set.")
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self, messages: list, tools: List = None, max_tokens: int = 1024):
        try:
            return self.client.chat.completions.create(
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.0,
                top_p=1.0,
                model=self.model,
                tools=tools,
                tool_choice="auto" if tools else None,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to get response from {'Azure OpenAI' if self.use_azure else 'OpenAI'}: {e}")

def build_prompt(place: str = "Taiwan") -> str:
    return f"I will be visiting {place} in summer and I want to know more about the local culture.\n"

if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(description="Query OpenAI or Azure OpenAI with a user input.")
    parser.add_argument("place", nargs="?", default="Taiwan", help="a place to visit, e.g., Taiwan")
    args = parser.parse_args()

    client = OpenAIClient()
    prompt = build_prompt(args.place)
    messages = [{"role": "user", "content": prompt}]
    response = client.get_response(messages)
    print(response.choices[0].message.content.strip())
