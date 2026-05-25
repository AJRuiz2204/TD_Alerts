"""
Monitor del modal de inactividad de Time Doctor.

Estrategia: en lugar de OCR sobre la pantalla, consulta directamente a la
API de Windows si existe una ventana cuyo titulo coincide con el modal y
ademas esta marcada como TOPMOST (forzada sobre todas las pantallas) o
tiene el foco. Consumo de CPU practicamente nulo.
"""

import sys
import time
import win32gui
import win32con
import winsound

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# ================= CONFIGURACION =================
# Lista de titulos posibles del modal (case-insensitive, coincidencia parcial).
# Anade aqui el titulo exacto que descubras con find_window.py.
TARGET_WINDOW_TITLES = [
    "Time Doctor",
    "Inactividad",
    "Are you still working",
    "Poca actividad",
]

# Intervalo entre chequeos. Como la consulta a la API es microsegundos,
# se puede bajar a 0.5s sin impacto.
CHECK_INTERVAL_SECONDS = 1.0

# Tras detectar el aviso y reproducir el sonido, cuanto esperar antes de
# volver a escanear (para no aturdir mientras se hace clic en "Si, sigo").
GRACE_PERIOD_SECONDS = 15

# Solo considerar la ventana detectada si es TOPMOST. Si es False, tambien
# acepta ventanas en foreground (mas sensible, mas falsos positivos).
REQUIRE_TOPMOST = True
# =================================================


def play_insistent_alert():
    print("\n[!] Modal de inactividad de Time Doctor detectado.")
    for _ in range(6):
        winsound.Beep(2500, 300)
        time.sleep(0.1)


def _matches_title(title):
    title_lower = title.lower()
    return any(t.lower() in title_lower for t in TARGET_WINDOW_TITLES)


def _window_predicate(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False

    title = win32gui.GetWindowText(hwnd)
    if not title or not _matches_title(title):
        return False

    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    is_topmost = bool(ex_style & win32con.WS_EX_TOPMOST)
    is_foreground = hwnd == win32gui.GetForegroundWindow()

    if REQUIRE_TOPMOST:
        return is_topmost
    return is_topmost or is_foreground


def is_modal_on_top():
    state = {"found": False}

    def callback(hwnd, _):
        if _window_predicate(hwnd):
            state["found"] = True
            return False
        return True

    try:
        win32gui.EnumWindows(callback, None)
    except win32gui.error:
        # EnumWindows lanza un error cuando el callback devuelve False para
        # detener la iteracion. Es esperado.
        pass

    return state["found"]


def main():
    print("Iniciando monitor de Time Doctor via Windows API.")
    print(f"Titulos buscados: {TARGET_WINDOW_TITLES}")
    print(f"Intervalo: {CHECK_INTERVAL_SECONDS}s | Require TOPMOST: {REQUIRE_TOPMOST}")
    print("Ctrl+C para salir.\n")

    try:
        while True:
            if is_modal_on_top():
                play_insistent_alert()
                time.sleep(GRACE_PERIOD_SECONDS)
            time.sleep(CHECK_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitor detenido.")
        sys.exit(0)


if __name__ == "__main__":
    main()
