# Taller / Curso OpenAI API

Este repositorio contiene un ejemplo básico de cómo utilizar la API de OpenAI con Python para el servicio de Chat Completions.

## Requisitos Previos

Asegúrate de tener instalado Python en tu sistema (preferiblemente Python 3.8 o superior).

## Paso 1: Configurar el Entorno Virtual (Recomendado)

Es una buena práctica utilizar un entorno virtual para instalar las dependencias de tu proyecto sin afectar a otras aplicaciones en tu sistema.

Abre tu terminal, navega a la carpeta principal del proyecto (donde se encuentra por ejemplo este archivo `README.md` y `requirements.txt`) y ejecuta:

```bash
# Navegar a la carpeta raíz del proyecto (si no estás ahí)
# cd ruta/a/curso-openai-api

# Crear el entorno virtual llamado "venv"
python3 -m venv venv

# Activar el entorno virtual (En Mac / Linux)
source venv/bin/activate
# (Si usas Windows, el comando es: venv\Scripts\activate)
```

## Paso 2: Instalar las Dependencias

El proyecto utiliza un archivo `requirements.txt` para gestionar las dependencias de forma estándar y replicable. Una vez activado tu entorno virtual (opcional pero recomendado), instálalas ejecutando:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Paso 3: Configurar las Variables de Entorno

El script utiliza un archivo `.env` para cargar la clave de la API de forma segura. 

1. Abre el archivo `.env` que se encuentra en la raíz del proyecto.
2. Asegúrate de que no haya espacios alrededor del signo igual para evitar problemas de lectura. Debe quedar exactamente así:

```env
OPENAI_API_KEY="sk-proj-tu_clave_aqui..."
```

*(El archivo actual ya ha sido configurado en tu proyecto con la sintaxis correcta).*

## Paso 4: Ejecutar el Script

Una vez que las dependencias están instaladas y tu clave configurada, puedes ejecutar el script:

```bash
python3 ChatCompletionAPI/script.py
```

Deberías ver en la consola la respuesta de la IA (PeterVision) interactuando contigo.
