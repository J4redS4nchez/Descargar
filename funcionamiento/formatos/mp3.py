# funcionamiento/formatos/mp3.py

import os
from yt_dlp import YoutubeDL

# Tu ruta de FFmpeg
FFMPEG_BIN = r"C:\Users\jaret\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"


def _obtener_nombre_libre_mp3(ruta_guardado: str, titulo: str) -> str:
    """
    Devuelve un nombre de archivo (sin extensión) que no exista aún:
    - Titulo
    - Titulo [1]
    - Titulo [2]
    ...
    """
    # Base sin extensión
    base = titulo.strip()
    if not base:
        base = "audio"

    # Primer intento: "Titulo.mp3"
    ruta_mp3 = os.path.join(ruta_guardado, f"{base}.mp3")
    if not os.path.exists(ruta_mp3):
        return base

    contador = 1
    while True:
        base_nueva = f"{base} [{contador}]"
        ruta_mp3 = os.path.join(ruta_guardado, f"{base_nueva}.mp3")
        if not os.path.exists(ruta_mp3):
            return base_nueva
        contador += 1


def descargar_mp3(URL: str, ruta_guardado: str, establecer_progreso=None):
    """
    Descarga audio y lo convierte a MP3 usando FFmpeg.
    Si el nombre ya existe, guarda como: "Nombre [1].mp3", "Nombre [2].mp3", etc.
    """

    if not URL or not ruta_guardado:
        print("[mp3] URL o ruta_guardado vacíos. No se descarga.")
        return

    os.makedirs(ruta_guardado, exist_ok=True)

    def gancho_progreso(datos):
        if not callable(establecer_progreso):
            return

        estado = datos.get("status")

        if estado == "downloading":
            total = datos.get("total_bytes") or datos.get("total_bytes_estimate")
            descargado = datos.get("downloaded_bytes")

            if total and descargado is not None and total > 0:
                establecer_progreso(descargado / total)

        elif estado == "finished":
            # Termina la descarga base; luego viene la conversión a mp3
            establecer_progreso(1.0)

    try:
        # 1) Sacar info (título) sin descargar
        with YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True}) as ydl:
            info = ydl.extract_info(URL, download=False)

        titulo = (info.get("title") or "audio").strip()

        # 2) Elegir un nombre libre (para evitar sobrescritura)
        nombre_base_libre = _obtener_nombre_libre_mp3(ruta_guardado, titulo)

        # 3) Usar esa base para TODO el proceso (descarga + conversión)
        outtmpl_base = os.path.join(ruta_guardado, f"{nombre_base_libre}.%(ext)s")

        opciones = {
            "outtmpl": outtmpl_base,
            "noplaylist": True,
            "progress_hooks": [gancho_progreso],

            # Bajar el mejor audio disponible
            "format": "bestaudio/best",

            # Convertir a mp3 con FFmpeg
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],

            "ffmpeg_location": FFMPEG_BIN,
            "quiet": True,
            "no_warnings": True,
        }

        print(f"[mp3] Iniciando descarga -> URL={URL} | ruta={ruta_guardado}")

        with YoutubeDL(opciones) as ydl:
            ydl.download([URL])

        print(f"[mp3] Descarga terminada (MP3): {nombre_base_libre}.mp3")

    except Exception as e:
        print(f"[mp3] Error descargando: {e}")