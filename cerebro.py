import requests
import json
import os
import time
from datetime import datetime

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_HISTORIAL = os.path.join(CARPETA, "historial.json")
ARCHIVO_MEMORIA   = os.path.join(CARPETA, "memoria.txt")
ARCHIVO_CONFIG    = os.path.join(CARPETA, "config.json")
MAX_HISTORIAL = 10

MODELOS_DISPONIBLES = {
    "1": {"nombre": "llama3.2:1b",    "descripcion": "Muy rapido, respuestas simples"},
    "2": {"nombre": "llama3.2",        "descripcion": "Equilibrado, recomendado"},
    "3": {"nombre": "llama3.1",        "descripcion": "Mas listo, mas lento"},
    "4": {"nombre": "mistral",         "descripcion": "Alternativa rapida y lista"},
    "5": {"nombre": "phi3",            "descripcion": "Muy ligero para PCs lentos"},
}

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def obtener_fecha_actual():
    ahora = datetime.now()
    dia_semana = DIAS[ahora.weekday()]
    return f"{dia_semana} {ahora.day} de {MESES[ahora.month - 1]} de {ahora.year}, {ahora.strftime('%H:%M')}h"

def elegir_modelo():
    if os.path.exists(ARCHIVO_CONFIG):
        with open(ARCHIVO_CONFIG, "r") as f:
            config = json.load(f)
            modelo = config.get("modelo")
            if modelo:
                print(f"✅ Usando modelo guardado: {modelo}")
                return modelo

    print("\n🧠 Elige el modelo de IA para JARVIS:")
    print("-" * 45)
    for key, val in MODELOS_DISPONIBLES.items():
        print(f"  {key} - {val['nombre']:<20} {val['descripcion']}")
    print(f"  6 - Otro                 Escribe el nombre tú mismo")
    print("-" * 45)

    while True:
        opcion = input("\nEscribe el número y pulsa Enter: ").strip()
        if opcion in MODELOS_DISPONIBLES:
            modelo = MODELOS_DISPONIBLES[opcion]["nombre"]
        elif opcion == "6":
            modelo = input("Escribe el nombre exacto del modelo (ej: llama3.2:3b): ").strip()
            if not modelo:
                print("Nombre no válido, inténtalo de nuevo.")
                continue
        else:
            print("Opción no válida, escribe un número del 1 al 6.")
            continue

        guardar = input(f"¿Guardar '{modelo}' como modelo por defecto? (s/n): ").strip().lower()
        if guardar == "s":
            config = {}
            if os.path.exists(ARCHIVO_CONFIG):
                with open(ARCHIVO_CONFIG, "r") as f:
                    config = json.load(f)
            config["modelo"] = modelo
            with open(ARCHIVO_CONFIG, "w") as f:
                json.dump(config, f)
            print(f"💾 Modelo guardado.")
        return modelo

def cambiar_modelo():
    if os.path.exists(ARCHIVO_CONFIG):
        os.remove(ARCHIVO_CONFIG)
    return elegir_modelo()

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
            historial = json.load(f)
            return historial[-MAX_HISTORIAL:]
    return []

def guardar_historial(historial):
    ultimos = historial[-MAX_HISTORIAL:]
    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(ultimos, f, ensure_ascii=False, indent=2)

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def guardar_memoria(dato):
    with open(ARCHIVO_MEMORIA, "a", encoding="utf-8") as f:
        f.write(f"- {dato}\n")

def detectar_dato_personal(texto_usuario):
    palabras_clave = ["me llamo", "mi nombre es", "tengo", "años", "vivo en", "trabajo"]
    for palabra in palabras_clave:
        if palabra in texto_usuario.lower():
            guardar_memoria(texto_usuario)
            break

def calentar_modelo(modelo):
    print(f"🔥 Cargando modelo {modelo} en memoria...")
    try:
        requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": modelo,
                "messages": [{"role": "user", "content": "hola"}],
                "stream": False,
                "system": "Responde solo: Listo."
            },
            timeout=60
        )
        print("✅ Modelo cargado.")
    except:
        print("⚠️ No se pudo calentar el modelo.")

def preguntar_a_ollama(texto, historial, modelo, contexto_web=None):
    memoria = cargar_memoria()
    fecha_actual = obtener_fecha_actual()

    system = f"""Eres JARVIS, el asistente personal de Iron Man. Responde siempre en español, de forma clara y concisa. Máximo 2 frases. Eres inteligente, educado y ligeramente formal. Cuando te den información de internet, úsala directamente para responder.

Fecha y hora actual: {fecha_actual}"""

    if memoria:
        system += f"\n\nCosas que sabes sobre el usuario:\n{memoria}"

    if contexto_web:
        mensaje = f"""El usuario pregunta: {texto}

Aquí tienes información actualizada de internet para responder:
{contexto_web}

IMPORTANTE: La fecha y hora actual es {fecha_actual}. Usa esta fecha para responder, ignora cualquier fecha anterior en la conversación."""
    else:
        mensaje = f"{texto}\n\n[Fecha y hora actual: {fecha_actual}]"

    historial.append({"role": "user", "content": mensaje})

    inicio = time.time()
    respuesta = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": modelo,
            "messages": historial[-MAX_HISTORIAL:],
            "stream": False,
            "system": system
        },
        timeout=60
    )
    print(f"⏱️ Ollama tardó: {time.time() - inicio:.1f} segundos")

    texto_respuesta = respuesta.json()["message"]["content"]
    historial.append({"role": "assistant", "content": texto_respuesta})

    detectar_dato_personal(texto)
    guardar_historial(historial)

    return texto_respuesta


