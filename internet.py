from ddgs import DDGS
import requests
import json
import os

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CONFIG = os.path.join(CARPETA, "config.json")

PALABRAS_CLAVE = [
    "noticia", "actual", "último", "últimas",
    "quién es", "cuándo", "precio",
    "busca", "buscar", "información sobre"
]

PALABRAS_TIEMPO = ["tiempo", "clima", "temperatura", "lluvia", "va a llover", "hace calor", "hace frío"]
PALABRAS_FECHA  = ["qué día", "qué fecha", "qué hora", "qué mes", "qué año"]

def obtener_ciudad_defecto():
    if os.path.exists(ARCHIVO_CONFIG):
        with open(ARCHIVO_CONFIG, "r") as f:
            config = json.load(f)
            return config.get("ciudad", None)
    return None

def guardar_ciudad_defecto(ciudad):
    config = {}
    if os.path.exists(ARCHIVO_CONFIG):
        with open(ARCHIVO_CONFIG, "r") as f:
            config = json.load(f)
    config["ciudad"] = ciudad
    with open(ARCHIVO_CONFIG, "w") as f:
        json.dump(config, f)
    print(f"💾 Ciudad guardada: {ciudad}")

def es_pregunta_tiempo(texto):
    return any(p in texto.lower() for p in PALABRAS_TIEMPO)

def necesita_internet(texto):
    texto_lower = texto.lower()
    if any(p in texto_lower for p in PALABRAS_FECHA):
        return False
    if any(p in texto_lower for p in PALABRAS_TIEMPO):
        return False
    return any(p in texto_lower for p in PALABRAS_CLAVE)

def buscar_tiempo(ciudad):
    try:
        respuesta = requests.get(
            f"https://wttr.in/{ciudad}?format=j1",
            timeout=5
        )
        datos = respuesta.json()
        actual = datos["current_condition"][0]
        temp = actual["temp_C"]
        sensacion = actual["FeelsLikeC"]
        descripcion = actual["weatherDesc"][0]["value"]
        humedad = actual["humidity"]
        return f"En {ciudad} hay {temp}°C, sensación de {sensacion}°C, {descripcion}, humedad {humedad}%"
    except Exception as e:
        print(f"Error obteniendo el tiempo: {e}")
        return None

def extraer_ciudad_del_texto(texto):
    ciudades_conocidas = [
        "madrid", "barcelona", "valencia", "sevilla", "zaragoza",
        "tarragona", "bilbao", "málaga", "alicante", "murcia",
        "granada", "toledo", "salamanca", "burgos", "lleida",
        "girona", "pamplona", "santander", "oviedo", "vigo"
    ]
    texto_lower = texto.lower()
    for c in ciudades_conocidas:
        if c in texto_lower:
            return c.capitalize()
    return None

def buscar_en_internet(pregunta, cast=None, hablar_fn=None):
    texto_lower = pregunta.lower()

    if any(p in texto_lower for p in PALABRAS_TIEMPO):
        ciudad = extraer_ciudad_del_texto(pregunta)

        if not ciudad:
            ciudad = obtener_ciudad_defecto()

        if not ciudad:
            if hablar_fn and cast is not None:
                hablar_fn("¿De qué ciudad quieres saber el tiempo?", cast)
            elif hablar_fn:
                hablar_fn("¿De qué ciudad quieres saber el tiempo?")

            from audio import escuchar_pregunta
            respuesta_ciudad = escuchar_pregunta()
            if respuesta_ciudad:
                ciudad = extraer_ciudad_del_texto(respuesta_ciudad)
                if not ciudad:
                    ciudad = respuesta_ciudad.strip().capitalize()

                guardar = input(f"¿Guardar '{ciudad}' como tu ciudad por defecto? (s/n): ").strip().lower()
                if guardar == "s":
                    guardar_ciudad_defecto(ciudad)
            else:
                ciudad = "Madrid"

        print(f"🌤️ Consultando tiempo en {ciudad}...")
        return buscar_tiempo(ciudad)

    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=3))
            if resultados:
                resumen = ""
                for r in resultados:
                    resumen += r["body"] + " "
                return resumen[:1500]
    except Exception as e:
        print(f"Error buscando: {e}")
    return None

