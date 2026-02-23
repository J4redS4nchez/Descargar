# Eemsik

**Eemsik** es una aplicación de escritorio para gestionar descargas (Short / MP3 / MP4) mediante una interfaz gráfica.

> Proyecto en desarrollo. Este repositorio contiene el código fuente, recursos y el script para generar instalador.

---

## Características

- Interfaz gráfica con componentes modulares.
- Soporte de descargas por formato:
  - Short
  - MP3
  - MP4
- Selector de ruta para guardar descargas (módulo `examinar`).
- Flujo de descarga separado por módulos (módulo `descargar` y `formatos`).
- Generación de instalador con **Inno Setup** (`instalador.iss`).
- Soporte con binarios externos en carpeta `bin/` (por ejemplo FFmpeg), según configuración del proyecto.

---

## Estructura del proyecto

Carpetas principales:

- `componentes/`  
  Componentes de la interfaz (URL, progreso, tarjetas, tooltip, switch de modo, etc.).

- `funcionamiento/`  
  Lógica principal del programa:
  - `formatos/` (mp3, mp4, short)
  - `descargar.py`
  - `examinar.py`
  - `analizar.py`

- `utils/`  
  Utilidades generales (por ejemplo `interfaz.py`).

- `assets/`  
  Recursos (iconos, imágenes, etc.). Incluye `assets/Logo.ico`.

Otros archivos relevantes:

- `main.py`  
  Punto de entrada de la aplicación.

- `ventana.py`  
  Ventana principal (clase `VentanaPrincipal`).

- `instalador.iss`  
  Script de Inno Setup para generar el instalador.

---

## Requisitos

- Windows 10/11 (recomendado si usas instalador / ejecutable).
- Python 3.x (si se ejecuta desde código).
- Dependencias de Python (según tu entorno/proyecto).







> Si aún no tienes `requirements.txt`, puedes generarlo así:
```bash
pip freeze > requirements.txt
