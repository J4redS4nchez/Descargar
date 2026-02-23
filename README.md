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

---

## Presentación

<img width="893" height="527" alt="presentacion_claro" src="https://github.com/user-attachments/assets/438ff7c6-1cb7-4285-b312-38e76c5c796c" />
<img width="900" height="527" alt="presentacion_oscuro" src="https://github.com/user-attachments/assets/5424b25d-4395-4df5-bb35-374529fc9836" />

---

## Interfaz

<img width="896" height="530" alt="interfaz_claro" src="https://github.com/user-attachments/assets/4aee67e6-07e3-4ccc-9e5d-7411fe6995f0" />
<img width="894" height="530" alt="interfaz_oscuro" src="https://github.com/user-attachments/assets/0b0e2c08-209c-40e5-b289-496aa7c74a07" />

---

## Lista desplegable

<img width="576" height="221" alt="lista_Claro" src="https://github.com/user-attachments/assets/9c1d24a1-2605-4098-9e60-2f2f0336ebee" />
<img width="548" height="155" alt="lista_oscuro" src="https://github.com/user-attachments/assets/fbc605db-96e6-4eee-93c2-4ea637c8981a" />

---

## Formato

<img width="138" height="164" alt="formato_claro" src="https://github.com/user-attachments/assets/95c8be27-cb39-4ea2-a9d0-2b0e19aa0005" />
<img width="138" height="164" alt="formato_oscuro" src="https://github.com/user-attachments/assets/658cbfa3-dbcb-45e3-b843-772ae4b468d8" />

---

## Barra de progreso

<img width="623" height="157" alt="barra_claro" src="https://github.com/user-attachments/assets/be25c80e-75ce-48df-8546-ba9b611e23b8" />
<img width="623" height="157" alt="barra_oscuro" src="https://github.com/user-attachments/assets/3d73898a-1a67-4cd9-8907-4b532e7f8d65" />

