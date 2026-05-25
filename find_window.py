"""
Detective: lista todas las ventanas visibles del sistema con su titulo,
estilos TOPMOST y si tienen el foco actualmente.

Ejecuta este script mientras el modal de inactividad de Time Doctor esta
visible en pantalla. Busca en la salida la linea marcada con [TOPMOST] o
[FOREGROUND] que corresponda al aviso, y copia ese titulo en monitor.py.
"""

import sys
import win32gui
import win32con

# Forzar UTF-8 en stdout para evitar UnicodeEncodeError con titulos de
# ventanas que contienen emojis o caracteres fuera de cp1252.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass


def enum_callback(hwnd, results):
    if not win32gui.IsWindowVisible(hwnd):
        return True

    title = win32gui.GetWindowText(hwnd)
    if not title:
        return True

    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    is_topmost = bool(ex_style & win32con.WS_EX_TOPMOST)
    is_foreground = hwnd == win32gui.GetForegroundWindow()

    tags = []
    if is_topmost:
        tags.append("TOPMOST")
    if is_foreground:
        tags.append("FOREGROUND")
    tag_str = f" [{', '.join(tags)}]" if tags else ""

    results.append((hwnd, title, tag_str))
    return True


def main():
    results = []
    win32gui.EnumWindows(enum_callback, results)

    print(f"Ventanas visibles detectadas: {len(results)}\n")
    for hwnd, title, tag_str in results:
        print(f"hwnd={hwnd:>10}  '{title}'{tag_str}")

    print(
        "\nBusca arriba la ventana del aviso de Time Doctor "
        "(probablemente con tag [TOPMOST] y/o [FOREGROUND])."
    )
    print("Copia su titulo exacto en la variable TARGET_WINDOW_TITLES de monitor.py.")


if __name__ == "__main__":
    main()
