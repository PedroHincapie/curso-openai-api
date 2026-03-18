import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""
    Obtiene la latitud y longitud de una ciudad
"""
def obtener_latitud_longitud_por_ciudad(ciudad):
    # 1. Definimos la URL y los parámetros
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": ciudad,
        "count": 1,        # Solo queremos el mejor resultado
        "language": "es",  # Opcional: nombres en español
        "format": "json"
    }

    # 2. Hacemos la petición
    response = requests.get(url, params=params)
    data = response.json()

    # 3. Validamos si hay resultados
    if "results" in data and len(data["results"]) > 0:
        primer_resultado = data["results"][0]
        
        # Open-Meteo usa 'latitude' y 'longitude' (no 'lat' y 'lon')
        lat = primer_resultado["latitude"]
        lon = primer_resultado["longitude"]
        pais = primer_resultado.get("country", "N/A")
        
        return {
            "latitud": lat,
            "longitud": lon,
            "pais": pais,
            "nombre": primer_resultado["name"]
        }
    else:
        return f"No se encontraron resultados para: {ciudad}"

"""
    Obtiene clima por latitud y longitud
"""
def obtener_clima_por_latitud_longitud(latitud: float, longitud: float):
    # 1. Definimos la URL y los parámetros
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "current": ["temperature_2m", "relative_humidity_2m", "is_day", "weather_code"],
        "timezone": "auto" # Ajusta la hora a la zona local de las coordenadas
    }

    # 3. Petición a la API
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Los datos actuales vienen dentro de la llave 'current'
        clima = data.get("current", {})
        
        return {
            "temperatura": clima.get("temperature_2m"),
            "unidad": data.get("current_units", {}).get("temperature_2m"),
            "humedad": clima.get("relative_humidity_2m"),
            "es_de_dia": bool(clima.get("is_day")),
            "codigo_clima": clima.get("weather_code")
        }
    else:
        return {"error": f"Error en la API: {response.status_code}"}


functions = [
    {
        "type": "function",
        "function": {
            "name": "obtener_latitud_longitud_por_ciudad",
            "description": "Usa esta funcion, para obtener la latitud y longitud de una ciudad",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Ciudad"
                    }
                },
                "required": ["ciudad"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_clima_por_latitud_longitud",
            "description": "Usa esta funcion, para obtener el clima de una ciudad por latitud y longitud",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitud": {
                        "type": "number",
                        "description": "Latitud de la ciudad"
                    },
                    "longitud": {
                        "type": "number",
                        "description": "Longitud de la ciudad"
                    }
                },
                "required": ["latitud", "longitud"]
            }
        }
    }
]

messages = [
    {
        "role": "system",
        "content": "Eres un asistente virtual que puede proporcionar información sobre el clima en diferentes ciudades, en tiempo real. "
    },
    {
        "role": "user",
        "content": "Cual es la temperatura actual en Medellin"
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(response.choices[0].message.content)
    
    
