from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from config import URL_AI_PROVIDER, DEFAULT_AI_MODEL
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url=URL_AI_PROVIDER,
    api_key=OPENROUTER_API_KEY
)

def getResponseFromAI(prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(
            model=DEFAULT_AI_MODEL,
            messages=messages
        )
        token_used = completion.usage.total_tokens
        print(f"Token used: {token_used}")
        return completion.choices[0].message.content
    except OpenAIError as e:
        print(f"An error occurred while communicating with the AI provider: {e}")
        return None