import pyautogui
import time

print("\n🔧 Herramienta de captura de coordenadas de mouse")
print("Coloca el mouse sobre el elemento deseado y espera 5 segundos...")

while True:
    input("\nPresiona ENTER cuando estés listo para capturar la posición actual del mouse...")
    time.sleep(5)
    position = pyautogui.position()
    print(f"📍 Coordenadas actuales → X = {position.x}, Y = {position.y}")
    print("-" * 40)
