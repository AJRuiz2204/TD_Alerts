# TDAlert - Monitor de Inactividad de Time Doctor

TDAlert es una herramienta ligera para Windows diseñada para detectar el modal de aviso de inactividad de **Time Doctor** y emitir una alerta sonora insistente. Su objetivo es prevenir que el usuario ignore accidentalmente el aviso de "Are you still working?" y pierda tiempo de registro.

## 🚀 Estrategia y Eficiencia

A diferencia de otras herramientas que utilizan OCR (Reconocimiento Óptico de Caracteres) o análisis de capturas de pantalla, TDAlert utiliza directamente la **API nativa de Windows (`win32gui`)**.

- **Consumo de CPU casi nulo:** Solo consulta el listado de ventanas del sistema en intervalos definidos.
- **Precisión:** Detecta ventanas marcadas como `TOPMOST` (siempre al frente) o que tienen el foco del sistema.
- **Ligereza:** No requiere librerías pesadas de procesamiento de imagen.

## 📋 Requisitos

- **Sistema Operativo:** Windows 10 o superior.
- **Python:** Versión 3.x instalada.

## 🔧 Instalación

1. **Clona este repositorio** o descarga los archivos en una carpeta local.
2. **Instala las dependencias** necesarias ejecutando el siguiente comando en tu terminal:

   ```bash
   pip install -r requirements.txt
   ```
   *(Esto instalará `pywin32`, necesario para interactuar con la API de Windows).*

## 📖 Guía de Uso

### 1. El Monitor Principal (`monitor.py`)
Es el script que debe permanecer ejecutándose mientras trabajas.

- **Ejecución:**
  ```bash
  python monitor.py
  ```
- **Funcionamiento:** Escaneará periódicamente las ventanas abiertas. Si detecta el aviso de Time Doctor, emitirá varios pitidos de alta frecuencia y pausará el escaneo durante 15 segundos (tiempo de gracia) para permitirte hacer clic en el modal sin que la alarma siga sonando.

### 2. Herramienta de Diagnóstico (`find_window.py`)
Si el monitor no detecta el aviso en tu sistema, es posible que el título de la ventana sea diferente.

- **Uso:** Ejecuta este script **mientras el aviso de Time Doctor sea visible** en pantalla:
  ```bash
  python find_window.py
  ```
- **Acción:** Busca en la salida una línea marcada con `[TOPMOST]` o `[FOREGROUND]`. Copia ese título exacto y añádelo a la lista de configuración en `monitor.py`.

## ⚙️ Configuración

Puedes personalizar el comportamiento editando las variables al inicio de `monitor.py`:

| Variable | Descripción | Defecto |
| :--- | :--- | :--- |
| `TARGET_WINDOW_TITLES` | Lista de títulos (o fragmentos) de ventana a buscar. | `["Time Doctor", "Inactividad", ...]` |
| `CHECK_INTERVAL_SECONDS` | Segundos entre cada escaneo del sistema. | `1.0` |
| `GRACE_PERIOD_SECONDS` | Segundos de silencio tras detectar una alerta. | `15` |
| `REQUIRE_TOPMOST` | Si es `True`, solo alerta si la ventana está "siempre al frente". | `True` |

---
**Nota:** Este proyecto es una utilidad independiente y no está afiliado oficialmente con Time Doctor.