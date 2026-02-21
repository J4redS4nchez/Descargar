# imagenes.py
# Funciones relacionadas con imágenes del proyecto (rutas, carga y preparación).

import os
from PIL import Image, ImageTk


#PRECARGA

def _obtener_de_precarga(clave: str):
    """
    Intenta obtener un recurso desde el módulo de precarga, si existe.
    Si no existe o falla el import, regresa None.
    """
    try:
        from precarga import obtener_recurso
        return obtener_recurso(clave)
    except Exception:
        return None


def obtener_ruta_logo_modo_luz() -> str:
    """
    Devuelve la ruta absoluta del logo en modo luz.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "Luz.png")


def cargar_logo_modo_luz(ancho_maximo: int = 320) -> ImageTk.PhotoImage:

    if ancho_maximo == 320:
        cacheado = _obtener_de_precarga("logo_luz_tk_320")
        if cacheado is not None:
            return cacheado

    """
    Carga el logo en modo luz manteniendo proporción.
    Se ajusta a un ancho máximo (ancho_maximo) y calcula el alto automáticamente.
    """
    ruta_logo = obtener_ruta_logo_modo_luz()
    imagen_logo = Image.open(ruta_logo)

    # Mantener proporción (sin deformar)
    ancho_original, alto_original = imagen_logo.size
    proporcion = ancho_original / alto_original

    ancho_nuevo = ancho_maximo
    alto_nuevo = int(ancho_nuevo / proporcion)

    imagen_logo = imagen_logo.resize((ancho_nuevo, alto_nuevo), Image.LANCZOS)
    return ImageTk.PhotoImage(imagen_logo)


def obtener_ruta_icono_luz() -> str:
    """
    Devuelve la ruta absoluta del icono (modo luz) para la tarjeta derecha.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "icono_luz.png")


def cargar_icono_luz_ctk(ancho: int = 170, alto: int = 230):


    if ancho == 170 and alto == 230:
        cacheado = _obtener_de_precarga("icono_luz_ctk_170x230")
        if cacheado is not None:
            return cacheado

    """
    Carga el icono (modo luz) como CTkImage para usarlo en CustomTkinter.
    Se redimensiona a (ancho, alto) manteniendo el control desde el caller.

    Nota:
    - Importamos customtkinter dentro de la función para no forzar la dependencia
      si este módulo se usa solo con Tkinter normal (por ejemplo, Presentacion).
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_luz()
    imagen_pil = Image.open(ruta_icono)

    # CTkImage se encarga de renderizar a tamaño 'size'
    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))


def obtener_ruta_icono_sol() -> str:
    """
    Devuelve la ruta absoluta del icono del sol.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "sol.png")


def obtener_ruta_icono_luna() -> str:
    """
    Devuelve la ruta absoluta del icono de la luna.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "luna.png")


def cargar_icono_sol_ctk(ancho: int = 14, alto: int = 14):

    if ancho == 14 and alto == 14:
        cacheado = _obtener_de_precarga("icono_sol_ctk_14x14")
        if cacheado is not None:
            return cacheado


    """
    Carga el icono del sol como CTkImage para CustomTkinter.
    Se escala a (ancho, alto).
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_sol()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))


def cargar_icono_luna_ctk(ancho: int = 14, alto: int = 14):


    if ancho == 14 and alto == 14:
        cacheado = _obtener_de_precarga("icono_luna_ctk_14x14")
        if cacheado is not None:
            return cacheado

    """
    Carga el icono de la luna como CTkImage para CustomTkinter.
    Se escala a (ancho, alto).
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_luna()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))



def obtener_ruta_icono_oscuro() -> str:
    """
    Devuelve la ruta absoluta del icono (modo oscuro) para la tarjeta derecha.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "icono_oscuro.png")


def cargar_icono_oscuro_ctk(ancho: int = 170, alto: int = 230):


    if ancho == 170 and alto == 230:
        cacheado = _obtener_de_precarga("icono_oscuro_ctk_170x230")
        if cacheado is not None:
            return cacheado

    """
    Carga el icono (modo oscuro) como CTkImage para usarlo en CustomTkinter.
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_oscuro()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))




def obtener_ruta_logo_modo_oscuro() -> str:
    """
    Devuelve la ruta absoluta del logo en modo oscuro.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))

    # Ajusta el nombre/extensión según tu archivo real en /assets
    return os.path.join(ruta_base, "assets", "oscuro.png")


def cargar_logo_modo_oscuro(ancho_maximo: int = 320) -> ImageTk.PhotoImage:

    if ancho_maximo == 320:
        cacheado = _obtener_de_precarga("logo_oscuro_tk_320")
        if cacheado is not None:
            return cacheado

    """
    Carga el logo en modo oscuro manteniendo proporción.
    Se ajusta a un ancho máximo (ancho_maximo) y calcula el alto automáticamente.
    """
    ruta_logo = obtener_ruta_logo_modo_oscuro()
    imagen_logo = Image.open(ruta_logo)

    # Mantener proporción (sin deformar)
    ancho_original, alto_original = imagen_logo.size
    proporcion = ancho_original / alto_original

    ancho_nuevo = ancho_maximo
    alto_nuevo = int(ancho_nuevo / proporcion)

    imagen_logo = imagen_logo.resize((ancho_nuevo, alto_nuevo), Image.LANCZOS)
    return ImageTk.PhotoImage(imagen_logo)


def cargar_logo_presentacion(ancho_maximo: int = 320) -> ImageTk.PhotoImage:
    """
    Carga el logo de la presentación según el modo actual (claro/oscuro).
    """
    import configuracion  # Import local para evitar problemas de importación circular

    if configuracion.MODO_OSCURO:
        return cargar_logo_modo_oscuro(ancho_maximo=ancho_maximo)

    return cargar_logo_modo_luz(ancho_maximo=ancho_maximo)



def obtener_ruta_icono_basura_claro() -> str:
    """
    Devuelve la ruta absoluta del icono de basura para modo claro.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "basura_claro.png")


def obtener_ruta_icono_basura_oscuro() -> str:
    """
    Devuelve la ruta absoluta del icono de basura para modo oscuro.

    Nota:
    - Soporta dos nombres posibles por si el archivo quedó como:
      'basura_oscuro.png' o 'basura_oscuro-png'
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))

    ruta_1 = os.path.join(ruta_base, "assets", "basura_oscuro.png")
    if os.path.exists(ruta_1):
        return ruta_1

    ruta_2 = os.path.join(ruta_base, "assets", "basura_oscuro-png")
    return ruta_2


def obtener_ruta_icono_descargar_claro() -> str:
    """
    Devuelve la ruta absoluta del icono de descargar para modo claro.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "descargar_claro.png")


def obtener_ruta_icono_descargar_oscuro() -> str:
    """
    Devuelve la ruta absoluta del icono de descargar para modo oscuro.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "descargar_oscuro.png")


def cargar_icono_basura_claro_ctk(ancho: int = 22, alto: int = 22):

    if ancho == 22 and alto == 22:
        cacheado = _obtener_de_precarga("icono_basura_claro_ctk_22x22")
        if cacheado is not None:
            return cacheado

    if ancho == 26 and alto == 26:
        cacheado = _obtener_de_precarga("icono_basura_claro_ctk_26x26")
        if cacheado is not None:
            return cacheado


    """
    Carga el icono de basura (modo claro) como CTkImage para CustomTkinter.
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_basura_claro()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))


def cargar_icono_basura_oscuro_ctk(ancho: int = 22, alto: int = 22):

    if ancho == 22 and alto == 22:
        cacheado = _obtener_de_precarga("icono_basura_oscuro_ctk_22x22")
        if cacheado is not None:
            return cacheado

    if ancho == 26 and alto == 26:
        cacheado = _obtener_de_precarga("icono_basura_oscuro_ctk_26x26")
        if cacheado is not None:
            return cacheado


    """
    Carga el icono de basura (modo oscuro) como CTkImage para CustomTkinter.
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_basura_oscuro()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))


def cargar_icono_descargar_ctk(tamanio=(22, 22)):
    """
    Carga el icono de descargar para usarlo en botones CTkButton.

    Importante:
    - No dependemos del appearance mode de CustomTkinter.
    - Usamos configuracion.MODO_OSCURO para elegir el archivo correcto.
    - El cache distingue entre modo claro y modo oscuro para que el icono cambie al vuelo.
    """
    from PIL import Image
    import customtkinter as ctk
    import configuracion

    # Definir clave de cache según el modo actual y el tamaño solicitado
    modo = "oscuro" if configuracion.MODO_OSCURO else "claro"
    clave_cache = f"icono_descargar_{modo}_ctk_{tamanio[0]}x{tamanio[1]}"

    # Intentar obtener desde precarga/cache si ya existe
    cacheado = _obtener_de_precarga(clave_cache)
    if cacheado is not None:
        return cacheado

    # Elegir ruta según el modo real de tu app
    if configuracion.MODO_OSCURO:
        ruta = obtener_ruta_icono_descargar_oscuro()
    else:
        ruta = obtener_ruta_icono_descargar_claro()

    imagen = Image.open(ruta)

    # Forzamos la misma imagen en light/dark para que NO cambie por el tema del sistema
    icono = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=tamanio)

    # Guardar en el cache para que futuras llamadas respeten el modo y no se regenere
    try:
        from precarga import guardar_recurso
        guardar_recurso(clave_cache, icono)
    except Exception:
        pass

    return icono




def obtener_ruta_icono_desplegar_claro() -> str:
    """
    Devuelve la ruta absoluta del icono de desplegar para modo claro.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "desplegar_claro.png")


def obtener_ruta_icono_desplegar_oscuro() -> str:
    """
    Devuelve la ruta absoluta del icono de desplegar para modo oscuro.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, "assets", "desplegar_oscuro.png")


def cargar_icono_desplegar_claro_ctk(ancho: int = 22, alto: int = 22):
    """
    Carga el icono de desplegar (modo claro) como CTkImage para CustomTkinter.
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_desplegar_claro()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))


def cargar_icono_desplegar_oscuro_ctk(ancho: int = 22, alto: int = 22):
    """
    Carga el icono de desplegar (modo oscuro) como CTkImage para CustomTkinter.
    """
    import customtkinter as ctk

    ruta_icono = obtener_ruta_icono_desplegar_oscuro()
    imagen_pil = Image.open(ruta_icono)

    return ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(ancho, alto))