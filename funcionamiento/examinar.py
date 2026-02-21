import os
import sys
import ctypes
from ctypes import wintypes
import uuid
import tkinter as tk
from tkinter import filedialog




def obtener_ruta_descargas():
    """
    Devuelve la ruta real de la carpeta Descargas en Windows usando Known Folders.

    Ventajas:
    - Funciona aunque el usuario haya movido Descargas a otra unidad.
    - No depende del idioma del sistema.

    Si no se puede obtener por alguna razón, usa un fallback razonable.
    """
    # Si no estamos en Windows, regresamos el home como fallback
    if sys.platform != "win32":
        return os.path.expanduser("~")

    try:
        # FOLDERID_Downloads = {374DE290-123F-4565-9164-39C4925E467B}
        folder_id = uuid.UUID("{374DE290-123F-4565-9164-39C4925E467B}")
        guid = (ctypes.c_ubyte * 16).from_buffer_copy(folder_id.bytes_le)

        path_ptr = wintypes.LPWSTR()
        shell32 = ctypes.windll.shell32

        # HRESULT SHGetKnownFolderPath(REFKNOWNFOLDERID, DWORD, HANDLE, PWSTR*)
        resultado = shell32.SHGetKnownFolderPath(guid, 0, None, ctypes.byref(path_ptr))
        if resultado != 0:
            raise OSError("SHGetKnownFolderPath falló")

        ruta = path_ptr.value
        ctypes.windll.ole32.CoTaskMemFree(path_ptr)
        return ruta

    except Exception:
        # Fallback típico si algo falla
        return os.path.join(os.path.expanduser("~"), "Downloads")





#FUNCIÓN EXAMINAR

def seleccionar_carpeta_guardado(ventana_padre=None, ruta_inicial=None):
    """
    Abre una ventana para seleccionar una carpeta de Windows.

    Parámetros:
    - ventana_padre: ventana principal (CTk/Tk) para que el diálogo se asocie correctamente.
    - ruta_inicial: carpeta inicial que mostrará el diálogo (si es válida).

    Retorna:
    - Ruta seleccionada (str) si el usuario eligió una carpeta.
    - Cadena vacía ("") si el usuario canceló.
    """
    # Si no se pasó una ruta inicial, usamos Descargas
    if not ruta_inicial:
        ruta_inicial = obtener_ruta_descargas()

    # Si la ruta inicial no existe, volvemos a Descargas como fallback
    if not isinstance(ruta_inicial, str) or not os.path.isdir(ruta_inicial):
        ruta_inicial = obtener_ruta_descargas()

    # Si no hay ventana padre, intentamos crear una temporal oculta
    ventana_temporal = None
    if ventana_padre is None:
        ventana_temporal = tk.Tk()
        ventana_temporal.withdraw()
        ventana_padre = ventana_temporal

    try:
        carpeta = filedialog.askdirectory(
            parent=ventana_padre,
            initialdir=ruta_inicial,
            title="Selecciona la carpeta donde se guardarán las descargas",
            mustexist=True
        )
        return carpeta if isinstance(carpeta, str) else ""
    finally:
        # Si creamos una ventana temporal, la destruimos
        if ventana_temporal is not None:
            ventana_temporal.destroy()