import threading
import http.server
import os
from datetime import datetime
from nest import conectar_nest
from internet import necesita_internet, buscar_en_internet, es_pregunta_tiempo
from cerebro import preguntar_a_ollama, cargar_historial, elegir_modelo, cambiar_modelo, calentar_modelo
from audio import escuchar_siempre, escuchar_pregunta, hablar

DIAS   = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES  = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
          "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def respuesta_directa(texto, cast):
    texto_lower = texto.lower()
    ahora = datetime.now()
    dia   = DIAS[ahora.weekday()]
    mes   = MESES[ahora.month - 1]

    if any(p in texto_lower for p in ["qué día", "que dia", "qué fecha", "que fecha"]):
        return f"Hoy es {dia}, {ahora.day} de {mes} de {ahora.year}."
    if any(p in texto_lower for p in ["qué hora", "que hora", "la hora"]):
        return f"Son las {ahora.strftime('%H:%M')}."
    if any(p in texto_lower for p in ["qué mes", "que mes"]):
        return f"Estamos en {mes} de {ahora.year}."
    if any(p in texto_lower for p in ["qué año", "que año"]):
        return f"Estamos en {ahora.year}."

    if es_pregunta_tiempo(texto_lower):
        print("🌤️ Pregunta de tiempo detectada.")
        datos = buscar_en_internet(texto, cast, hablar)
        if datos:
            return datos
        return "No he podido obtener el tiempo en este momento."

    return None

def iniciar_servidor():
    os.chdir("C:\\Users\\Public")
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("", 8765), handler)
    httpd.serve_forever()

hilo = threading.Thread(target=iniciar_servidor, daemon=True)
hilo.start()

cast = conectar_nest()
modelo = elegir_modelo()
calentar_modelo(modelo)

historial = cargar_historial()
print(f"\n✅ JARVIS en espera con modelo {modelo}...")
print("Di 'Jarvis' para activarlo.")
print("Di 'Jarvis cambia modelo' para cambiar la IA.")
print("(Escribe Ctrl+C para apagar)\n")

FRASES_CAMBIO = ["cambia modelo", "cambiar modelo", "cambia el modelo", "cambiar el modelo"]
FRASES_PARAR  = ["para", "stop", "detente", "cállate"]

while True:
    try:
        texto = escuchar_siempre()

        if texto and "jarvis" in texto:

            if any(frase in texto for frase in FRASES_CAMBIO):
                modelo = cambiar_modelo()
                calentar_modelo(modelo)
                hablar(f"Modelo cambiado a {modelo}", cast)
                continue

            print("💡 Palabra de activación detectada.")
            hablar("Dígame", cast)
            pregunta = escuchar_pregunta()

            if not pregunta:
                continue

            if any(frase in pregunta.lower() for frase in FRASES_CAMBIO):
                modelo = cambiar_modelo()
                calentar_modelo(modelo)
                hablar(f"Modelo cambiado a {modelo}", cast)
                continue

            if any(frase in pregunta.lower() for frase in FRASES_PARAR):
                hablar("De acuerdo.", cast)
                continue

            respuesta = respuesta_directa(pregunta, cast)
            if respuesta:
                print(f"⚡ Respuesta directa: {respuesta}")
                hablar(respuesta, cast)
                continue

            contexto_web = None
            if necesita_internet(pregunta):
                print("🌐 Buscando en internet...")
                contexto_web = buscar_en_internet(pregunta, cast, hablar)

            respuesta = preguntar_a_ollama(pregunta, historial, modelo, contexto_web)
            hablar(respuesta, cast)

    except KeyboardInterrupt:
        print("\n👋 JARVIS apagado. Hasta luego.")
        break


