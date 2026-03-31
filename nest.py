import pychromecast
from pychromecast.models import CastInfo, HostServiceInfo
import uuid

IP_NEST = "192.168.1.XXX"

def conectar_nest():
    while True:
        print("🔍 Conectando con el Nest Mini...")
        try:
            servicio = HostServiceInfo(host=IP_NEST, port=8009)
            info = CastInfo(
                services={servicio},
                uuid=uuid.uuid4(),
                model_name="Google Home Mini",
                friendly_name="Jarvis",
                host=IP_NEST,
                port=8009,
                cast_type="audio",
                manufacturer="Google"
            )
            cast = pychromecast.Chromecast(cast_info=info)
            cast.wait(timeout=5)
            if not cast.is_idle:
                raise Exception("No se pudo establecer conexión")
            print("✅ Nest Mini conectado.")
            return cast
        except Exception as e:
            print(f"\n⚠️ No se pudo conectar con el Nest Mini.")
            print("\n¿Qué quieres hacer?")
            print("  1 - Volver a intentarlo")
            print("  2 - Continuar con los altavoces del portátil")
            opcion = input("\nEscribe 1 o 2 y pulsa Enter: ").strip()
            if opcion == "2":
                print("▶️ Usando altavoces del portátil.")
                return None
            print("\n🔄 Reintentando...\n")
