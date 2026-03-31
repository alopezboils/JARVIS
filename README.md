# JARVIS
# 🤖 JARVIS — Asistente Personal por Voz

Un asistente personal de voz inspirado en JARVIS de Iron Man, que corre completamente en tu ordenador de forma **gratuita y sin suscripciones**.

---

## ✨ ¿Qué puede hacer?

| Función | Cómo activarla |
|---|---|
| 🎤 Escuchar tu voz | Habla cuando veas "Escuchando..." |
| 💡 Activarse | Di **"Jarvis"** |
| 💬 Responder preguntas | Di "Jarvis" → espera "Dígame" → habla |
| 🌤️ Tiempo actual | "Jarvis, ¿qué tiempo hace?" |
| 📅 Fecha y hora | "Jarvis, ¿qué día es hoy?" / "¿qué hora es?" |
| 🌐 Buscar en internet | "Jarvis, busca información sobre..." |
| 🧠 Recordar tu nombre | "Jarvis, me llamo [nombre]" |
| 🔄 Cambiar modelo de IA | Di "Jarvis, cambia modelo" |
| ⏹️ Parar una respuesta | Pulsa la tecla **Espacio** |

---

## 🖥️ Requisitos

- Windows 10 o 11
- Python 3.10 o superior → [descargar](https://python.org)
- Ollama → [descargar](https://ollama.com)
- Micrófono (el del portátil sirve)
- Altavoz (opcional: Google Nest Mini)
- Conexión a internet (para búsquedas y tiempo)

---

## 🚀 Instalación paso a paso

### 1. Instalar Python
Ve a [python.org](https://python.org), descarga e instala Python 3.10 o superior.

### 2. Instalar Ollama
Ve a [ollama.com](https://ollama.com), descarga e instala Ollama para Windows.

### 3. Descargar el modelo de IA
Abre una terminal (Windows + R → escribe `cmd` → Enter) y ejecuta:
```
ollama pull llama3.2:1b
```

### 4. Descargar JARVIS
Descarga o clona este repositorio en tu ordenador:
```
git clone https://github.com/TU_USUARIO/JARVIS.git
cd JARVIS
```

### 5. Instalar las librerías
En la terminal, dentro de la carpeta JARVIS ejecuta:
```
pip install speechrecognition pyaudio anthropic requests duckduckgo-search pychromecast gtts mutagen keyboard ddgs
```

### 6. ¡Arrancar JARVIS!
```
python jarvis.py
```

La primera vez te preguntará:
- **Qué modelo de IA** quieres usar
- **Tu ciudad** (cuando preguntes el tiempo por primera vez)

---

## 📁 Estructura del proyecto

```
📁 JARVIS
   📄 jarvis.py       ← Script principal, arranca desde aquí
   📄 audio.py        ← Micrófono y altavoces
   📄 cerebro.py      ← Inteligencia con Ollama
   📄 internet.py     ← Búsquedas web y tiempo
   📄 nest.py         ← Conexión Google Nest Mini (opcional)
   📄 config.json     ← Configuración guardada (se crea automáticamente)
   📄 historial.json  ← Historial de conversaciones (se crea automáticamente)
   📄 memoria.txt     ← Memoria persistente (se crea automáticamente)
```

---

## 🧠 Modelos de IA disponibles

| Opción | Modelo | Velocidad | Calidad |
|---|---|---|---|
| 1 | llama3.2:1b | ⚡⚡⚡ Muy rápido | ⭐⭐ |
| 2 | llama3.2 | ⚡⚡ Rápido | ⭐⭐⭐ |
| 3 | llama3.1 | ⚡ Normal | ⭐⭐⭐⭐ |
| 4 | mistral | ⚡⚡ Rápido | ⭐⭐⭐ |
| 5 | phi3 | ⚡⚡⚡ Muy rápido | ⭐⭐ |
| 6 | Otro | — | — |

Para cambiar el modelo en cualquier momento di **"Jarvis, cambia modelo"**.

---

## 🔊 Google Nest Mini (opcional)

Si tienes un Google Nest Mini puedes usarlo como altavoz de JARVIS.

1. Asegúrate de que está en la **misma red WiFi** que tu ordenador
2. Abre la app **Google Home** → ajustes del dispositivo → anota la **IP**
3. Abre `nest.py` y cambia esta línea con tu IP:
```python
IP_NEST = "192.168.1.XXX"
```

---

## ⌨️ Controles

| Acción | Cómo |
|---|---|
| Activar JARVIS | Di **"Jarvis"** |
| Parar respuesta | Pulsa **Espacio** |
| Cambiar modelo | Di **"Jarvis, cambia modelo"** |
| Apagar JARVIS | **Ctrl + C** en la terminal |

---

## 💾 Archivos que se crean automáticamente

- `config.json` — guarda tu modelo y ciudad preferidos
- `historial.json` — guarda las últimas 10 conversaciones
- `memoria.txt` — guarda datos personales que le cuentes a JARVIS

---

## 🛠️ Problemas frecuentes

**"No te he entendido" muy seguido**
→ Habla más claro y cerca del micrófono. Puedes subir `phrase_time_limit` en `audio.py`.

**JARVIS tarda mucho en responder**
→ Cambia al modelo `llama3.2:1b` (opción 1). Es el más rápido.

**No conecta con el Nest Mini**
→ Comprueba que está encendido y en la misma red WiFi. Puedes continuar sin él usando los altavoces del portátil.

**Error al instalar pyaudio**
→ Descarga el archivo .whl desde [aquí](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) e instálalo manualmente.

---

## 📜 Licencia

MIT — Libre para usar, modificar y compartir.
