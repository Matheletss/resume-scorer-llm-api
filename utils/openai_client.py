from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads .env from root
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_completion(messages, model="gpt-4o-mini-2024-07-18", temperature=0.0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content