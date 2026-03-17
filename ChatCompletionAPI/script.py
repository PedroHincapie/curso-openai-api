import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(client)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Te llamas PeterVision, presentate como tal y dime en que puedo ayudarte"},
        {"role": "user", "content": "Hola, ¿cómo estás?"},
    ],
)

print(response.choices[0].message.content)  