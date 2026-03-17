import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(client)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Te llamas PeterVision, presentate como tal y dime en que puedo ayudarte"
        },
        {
            "role": "user",
            "content": "Hola, ¿cómo estás?"
        },
        {
            "role": "assistant",
            "content": "¡Hola! Soy PeterVision, un asistente aquí para ayudarte. ¿En qué puedo asistirte hoy?"
        },
        {
            "role": "user",
            "content": "Que es la inteligencia artificial?, explicalo como si fuera para un niño de 5 años"
        },
        
    ],
)

print(response.choices[0].message.content)  