# funcionamiento/formatos/mp3.py

import os
from yt_dlp import YoutubeDL

# Tu ruta de FFmpeg (misma que usaste en short/mp4)
FFMPEG_BIN = r"C:\Users\jaret\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"


def descargar_mp3(URL: str, ruta_guardado: str, establecer_progreso=None):
    """
    Descarga audio y lo convierte a MP3 usando FFmpeg.
    """

    if not URL or not ruta_guardado:
        print("[mp3] URL o ruta_guardado vacíos. No se descarga.")
        return

    os.makedirs(ruta_guardado, exist_ok=True)

    def gancho_progreso(datos):
        """
        Hook de progreso de yt-dlp para actualizar la barra.
        """
        if not callable(establecer_progreso):
            return

        estado = datos.get("status")

        if estado == "downloading":
            total = datos.get("total_bytes") or datos.get("total_bytes_estimate")
            descargado = datos.get("downloaded_bytes")

            if total and descargado is not None and total > 0:
                establecer_progreso(descargado / total)

        elif estado == "finished":
            # Ojo: aquí "finished" es cuando termina de bajar el archivo base,
            # luego FFmpeg convierte a mp3. Lo dejamos en 100% igual.
            establecer_progreso(1.0)

    opciones = {
        # El nombre final quedará con extensión mp3 después del postprocesado
        "outtmpl": os.path.join(ruta_guardado, "%(title).200s.%(ext)s"),
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

    try:
        print(f"[mp3] Iniciando descarga -> URL={URL} | ruta={ruta_guardado}")

        with YoutubeDL(opciones) as ydl:
            ydl.download([URL])

        print("[mp3] Descarga terminada (MP3).")

    except Exception as e:
        print(f"[mp3] Error descargando: {e}")