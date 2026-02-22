# funcionamiento/formatos/short.py

import os
from yt_dlp import YoutubeDL

# Tu ruta de FFmpeg (ajústala si cambia)
FFMPEG_BIN = r"C:\Users\jaret\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"


def descargar_short(URL, ruta_guardado, establecer_progreso=None):
    """
    Descarga un short en MP4 (H.264 + audio) a la ruta indicada.
    Evita AV1 para que Windows lo reproduzca sin pedir códec.
    """

    if not URL or not ruta_guardado:
        print("[short] URL o ruta_guardado vacíos. No se descarga.")
        return

    os.makedirs(ruta_guardado, exist_ok=True)

    if callable(establecer_progreso):
        establecer_progreso(0.0)

    def gancho_progreso(datos):
        if not callable(establecer_progreso):
            return

        if datos.get("status") == "downloading":
            total = datos.get("total_bytes") or datos.get("total_bytes_estimate")
            descargado = datos.get("downloaded_bytes")

            if total and descargado is not None and total > 0:
                establecer_progreso(descargado / total)

        elif datos.get("status") == "finished":
            establecer_progreso(1.0)

    opciones = {
        "outtmpl": os.path.join(ruta_guardado, "%(title).200s.%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [gancho_progreso],

        # ✅ FORZAR H.264 (avc1) en MP4 + audio M4A
        # - Esto evita que yt-dlp elija AV1 aunque sea mp4
        "format": "bv*[vcodec^=avc1][ext=mp4]+ba[ext=m4a]/b[vcodec^=avc1][ext=mp4]/b[ext=mp4]/best",

        # ✅ Forzar salida mp4 al fusionar
        "merge_output_format": "mp4",

        # ✅ Para fusionar correctamente (y evitar archivos raros)
        "ffmpeg_location": FFMPEG_BIN,

        "quiet": True,
        "no_warnings": True,
    }

    try:
        print(f"[short] Iniciando descarga -> URL={URL} | ruta={ruta_guardado}")

        with YoutubeDL(opciones) as ydl:
            ydl.download([URL])

        print("[short] Descarga terminada (MP4 H.264).")

    except Exception as e:
        print(f"[short] Error descargando: {e}")

    finally:
        if callable(establecer_progreso):
            establecer_progreso(0.0)