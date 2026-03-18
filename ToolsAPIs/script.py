import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {
        "role": "system",
        "content": "Eres un asistente virtual que puede proporcionar información sobre el clima en diferentes ciudades, en tiempo real. "
    },
    {
        "role": "user",
        "content": "Cual es la temperatura actual en Medellin Colombia"
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(response.choices[0].message.content)
    
    
