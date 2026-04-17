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

def getResponseFromOpenAI(prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = client.responses.create(
            model=DEFAULT_AI_MODEL,
            input=messages
        )
        return response
    except OpenAIError as e:
        print(f"An error occurred while communicating with the AI provider: {e}")
        return None