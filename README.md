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

## 🤝 Cómo Contribuir

¡Las contribuciones son bienvenidas! Este proyecto sigue el flujo estándar de **Fork & Pull Request**. La rama `main` está protegida: no se aceptan pushes directos y todos los cambios deben pasar por revisión y por los checks de Code Scanning.

### Flujo de trabajo

1. **Haz fork** del repositorio desde GitHub.
2. **Clona tu fork** localmente:
   ```bash
   git clone git@github.com:<tu-usuario>/TD_Alerts.git
   cd TD_Alerts
   ```
3. **Configura el remoto upstream** para mantener tu fork sincronizado:
   ```bash
   git remote add upstream git@github.com:AJRuiz2204/TD_Alerts.git
   ```
4. **Crea una rama descriptiva** desde `main` actualizada:
   ```bash
   git fetch upstream
   git checkout -b feat/mi-cambio upstream/main
   ```
   Usa prefijos como `feat/`, `fix/`, `docs/`, `refactor/` o `chore/`.
5. **Realiza tus cambios** y haz commits atómicos con mensajes claros (en español o inglés). Sigue el estilo del historial existente.
6. **Verifica localmente** que `monitor.py` y `find_window.py` siguen funcionando antes de enviar el PR.
7. **Push a tu fork**:
   ```bash
   git push origin feat/mi-cambio
   ```
8. **Abre un Pull Request** contra `main` del repositorio original. En la descripción incluye:
   - Qué problema resuelve o qué funcionalidad añade.
   - Cómo probaste el cambio (escenario reproducible).
   - Capturas o logs si aplica.
9. **Espera los checks**: el PR debe pasar Code Scanning y al menos una revisión aprobatoria antes de poder fusionarse.

### Convenciones

- **Estilo:** Mantén el código simple y dependiente solo de la API nativa de Windows (`win32gui`). Evita introducir dependencias pesadas (OCR, ML, etc.) salvo discusión previa en un issue.
- **Compatibilidad:** El objetivo es Windows 10+ con Python 3.x. No rompas esa base.
- **Issues primero:** Para cambios grandes (nuevas funciones, refactors mayores) abre un issue antes para discutir el enfoque y evitar trabajo desperdiciado.
- **Una cosa por PR:** Mantén los PRs enfocados; es más fácil revisar y fusionar cambios pequeños.

### Reportar bugs o pedir features

Abre un issue en [GitHub Issues](https://github.com/AJRuiz2204/TD_Alerts/issues) describiendo:
- Versión de Windows y de Python.
- Pasos para reproducir (o título exacto de la ventana detectada con `find_window.py` si es un problema de detección).
- Comportamiento esperado vs. comportamiento observado.

---
**Nota:** Este proyecto es una utilidad independiente y no está afiliado oficialmente con Time Doctor.