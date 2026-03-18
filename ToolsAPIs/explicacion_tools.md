# Explicación del Script de Tool Calling

Este documento explica paso a paso y línea por línea el funcionamiento del archivo `script.py` dentro de la carpeta `ToolsAPIs`. El objetivo de este script es demostrar cómo la Inteligencia Artificial puede interactuar con el mundo real utilizando **Tool Calling** (Llamada a Herramientas).

---

## 1. Importación de Librerías y Configuración

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
```
* **`os` y `dotenv`**: Permiten leer las variables de entorno desde el archivo `.env`, manteniendo nuestra `OPENAI_API_KEY` segura y fuera del código.
* **`OpenAI`**: Es la librería oficial de OpenAI que nos facilita la comunicación con su API.
* **`requests`**: Sirve para hacer peticiones HTTP a APIs externas (en este caso, a las APIs de Open-Meteo para obtener las coordenadas y el clima).
* **`json`**: La utilizamos para convertir los argumentos que nos envía la IA (en formato texto/JSON) a diccionarios de Python y viceversa.

```python
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```
* Inicializamos el cliente de OpenAI pasándole nuestra clave de autenticación.

---

## 2. Definición de Herramientas Locales (Python)

Antes de decirle a la IA qué herramientas existen, nosotros debemos programar localmente las funciones que realizarán el trabajo real.

```python
def obtener_latitud_longitud_por_ciudad(ciudad):
    ...
```
* Esta función recibe el nombre de una ciudad como texto.
* Hace una petición a la API gratuita de *geocoding* de Open-Meteo.
* Devuelve un diccionario o JSON con la `latitud`, `longitud`, `país` y `nombre` exacto de la ciudad. Es un paso necesario porque las APIs de clima suelen requerir coordenadas, no nombres.

```python
def obtener_clima_por_latitud_longitud(latitud: float, longitud: float):
    ...
```
* Esta función recibe las coordenadas numéricas obtenidas en el paso anterior.
* Hace la consulta a la API del clima de Open-Meteo y devuelve la `temperatura`, `humedad` y otras métricas reales de esa zona geográfica.

---

## 3. Describiendo las Herramientas a la IA (El Schema)

La IA no puede ejecutar código Python directamente. Necesita que le expliquemos *qué puede hacer*, *cómo se llama la función* y *qué parámetros necesita*. Esto se hace con un arreglo llamado `functions`:

```python
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
    ...
]
```
* **`name`**: El nombre exacto de la herramienta. La IA nos devolverá este nombre si decide usarla.
* **`description`**: Súper importante. Es la instrucción que lee el modelo para decidir si la herramienta le sirve para responder a la pregunta del usuario.
* **`parameters`**: El formato exacto en el que queremos que la IA nos entregue la información extraída del mensaje del usuario.

---

## 4. El Historial de Mensajes y Roles

```python
messages = [
    {
        "role": "system",
        "content": "Eres un asistente virtual que puede proporcionar información sobre el clima en diferentes ciudades, en tiempo real. "
    },
    {
        "role": "user",
        "content": "Cual es la temperatura actual en Pasto"
    }
]
```
Cada mensaje tiene un `role` (rol) específico:
* **`system`**: Define la personalidad y el propósito del modelo. Aquí lo preparamos psicológicamente para que entienda que es un experto en clima.
* **`user`**: La consulta directa del usuario humano.
* **`assistant`** (se verá más adelante): Las respuestas que da el propio modelo.
* **`tool`** (se verá más adelante): El rol que usamos para devolver a la IA la información obtenida por las herramientas.

---

## 5. El Bucle de Ejecución (El Corazón del Tool Calling)

Dado que la IA puede necesitar usar varias herramientas (por ejemplo: primero buscar coordenadas, recibirlas, luego buscar clima, recibirlo y finalmente responder), debemos usar un bucle `while True:` para mantener la conversación viva hasta obtener la respuesta final.

```python
while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=functions,
        tool_choice="auto"    
    )
```
* Enviamos la consulta actualizando siempre la lista de `messages`.
* Mandamos nuestra lista de `tools` disponibles.
* `tool_choice="auto"` deja que el modelo decida por su cuenta si usa una herramienta o si usa lenguaje natural.

```python
    response_message = response.choices[0].message
    
    # 1. Agregamos la intención de la IA a la conversación
    if response_message.tool_calls:
        messages.append(response_message)
```
* Si la IA responde solicitando una herramienta, debemos guardar *esa petición* en el historial para no perder el hilo.

```python
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
```
* Iteramos sobre las solicitudes de la IA. Extraemos qué función quiere invocar y convertimos el texto JSON de sus argumentos a un diccionario de Python.

```python
            if function_name == "obtener_latitud_longitud_por_ciudad":
                function_response = function_to_call(ciudad=function_args.get("ciudad"))
```
* Aquí nuestro código "hace puente". Ejecutamos la función real escrita al principio del script pasándole los valores que dedujo la IA ("Pasto").

```python
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )
```
* Mando el resultado *de vuelta* al cerebro del modelo. Notar que el rol es `"tool"`, y le paso el `tool_call_id` original para que la IA sepa que este mensaje es la respuesta de la función que acaba de invocar.
* Tras esto, el bucle `while` se repite con el nuevo historial.

```python
    else:
        # Si no hay llamadas a herramientas
        print("--- Respuesta Final de la IA ---")
        print(response_message.content)
        break
```
* Si el modelo nos envía una respuesta en texto natural y `tool_calls` está vacío, significa que ya tiene toda la información que necesita. Imprime la solución y rompemos el ciclo con `break`.
