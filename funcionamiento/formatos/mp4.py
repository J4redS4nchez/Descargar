# funcionamiento/formatos/mp4.py

import os
from yt_dlp import YoutubeDL
from utils.interfaz import obtener_ruta_ffmpeg

# Tu ruta de FFmpeg (misma que usaste en short)
FFMPEG_BIN = obtener_ruta_ffmpeg()


def descargar_mp4(URL: str, ruta_guardado: str, establecer_progreso=None):
    """
    Descarga un video de YouTube en MP4 (H.264 + audio) a la ruta indicada.
    Evita AV1 para que Windows lo reproduzca sin pedir códec.
    """

    if not URL or not ruta_guardado:
        print("[mp4] URL o ruta_guardado vacíos. No se descarga.")
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
            establecer_progreso(1.0)

    opciones = {
        "outtmpl": os.path.join(ruta_guardado, "%(title).200s.%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [gancho_progreso],
        "overwrites": False,

        # Forzar H.264 (avc1) en MP4 + audio M4A
        "format": "bv*[vcodec^=avc1][ext=mp4]+ba[ext=m4a]/b[vcodec^=avc1][ext=mp4]/b[ext=mp4]/best",

        # Forzar salida mp4 al fusionar
        "merge_output_format": "mp4",

        # Usar FFmpeg para fusionar audio/video correctamente
        "ffmpeg_location": FFMPEG_BIN,

        "quiet": True,
        "no_warnings": True,
    }

    try:
        print(f"[mp4] Iniciando descarga -> URL={URL} | ruta={ruta_guardado}")

        with YoutubeDL(opciones) as ydl:
            ydl.download([URL])

        print("[mp4] Descarga terminada (MP4 H.264).")

    except Exception as e:
        print(f"[mp4] Error descargando: {e}")