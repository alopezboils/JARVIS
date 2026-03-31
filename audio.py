import speech_recognition as sr
import subprocess
import tempfile
import os
import socket
import time
import threading
import keyboard
from gtts import gTTS
from mutagen.mp3 import MP3

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def escuchar_siempre():
    r = sr.Recognizer()
    with sr.Microphone() as fuente:
        r.adjust_for_ambient_noise(fuente, duration=1)
        try:
            audio = r.listen(fuente, timeout=3, phrase_time_limit=10)
            texto = r.recognize_google(audio, language="es-ES").lower()
            return texto
        except:
            return None

def escuchar_pregunta():
    r = sr.Recognizer()
    r.pause_threshold = 2.0
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 1.5
    with sr.Microphone() as fuente:
        print("🎤 ¿Qué necesitas?")
        r.adjust_for_ambient_noise(fuente, duration=1)
        try:
            audio = r.listen(fuente, timeout=5, phrase_time_limit=15)
            texto = r.recognize_google(audio, language="es-ES")
            print(f"Tú dijiste: {texto}")
            return texto
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("No te he entendido.")
            return None

def obtener_duracion_audio(archivo):
    try:
        audio = MP3(archivo)
        return audio.info.length
    except:
        return len(open(archivo, "rb").read()) / 16000

def hablar(texto, cast=None):
    print(f"JARVIS: {texto}")
    print("(Pulsa ESPACIO para interrumpir)")

    if cast:
        try:
            ip_local = obtener_ip_local()
            temp = tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp3", dir="C:\\Users\\Public"
            )
            nombre_temp = temp.name
            temp.close()

            resultado = {"listo": False}

            def generar_audio():
                tts = gTTS(texto, lang="es")
                tts.save(nombre_temp)
                resultado["listo"] = True

            hilo_tts = threading.Thread(target=generar_audio)
            hilo_tts.start()

            print("⏳ Generando audio...")
            hilo_tts.join(timeout=10)

            if not resultado["listo"]:
                raise Exception("Timeout generando audio")

            nombre_archivo = os.path.basename(nombre_temp)
            url_audio = f"http://{ip_local}:8765/{nombre_archivo}"
            mc = cast.media_controller
            mc.play_media(url_audio, "audio/mp3")
            mc.block_until_active(timeout=10)
            duracion = obtener_duracion_audio(nombre_temp)
            print(f"⏳ Reproduciendo {duracion:.1f} segundos...")

            inicio = time.time()
            while time.time() - inicio < duracion + 0.5:
                if keyboard.is_pressed("space"):
                    mc.stop()
                    print("⏹️ Respuesta detenida.")
                    time.sleep(0.5)
                    return
                time.sleep(0.1)
            return
        except Exception as e:
            print(f"Error con Nest Mini: {e}, usando altavoces del portátil.")

    proceso = subprocess.Popen(
        ["powershell", "-Command", f"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Speak(@'
{texto}
'@)
"""]
    )

    while proceso.poll() is None:
        if keyboard.is_pressed("space"):
            proceso.terminate()
            print("⏹️ Respuesta detenida.")
            time.sleep(0.5)
            return
        time.sleep(0.1)

