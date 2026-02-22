# componentes/tooltip.py

import customtkinter as ctk
import configuracion


def mostrar_tooltip(frame_padre, mensaje: str, duracion_ms: int = 5000):
    """
    Muestra una tarjetita (tooltip) dentro del frame_padre, con auto-ocultado.

    Reglas de color (como pediste):
    - Contorno y relleno del tooltip:
        * modo claro: azul (mismo que texto "URL")
        * modo oscuro: color del texto "URL" en oscuro
      (esto ya lo da configuracion.COLOR_TEXTO_URL según el modo)
    - Texto dentro del tooltip:
        * modo claro: color del fondo de ventana claro
        * modo oscuro: color del fondo de ventana oscuro
      (esto ya lo da configuracion.COLOR_FONDO_VENTANA según el modo)
    """

    if frame_padre is None:
        return

    # Cancelar temporizador previo si existe
    after_id = getattr(frame_padre, "_tooltip_after_id", None)
    if after_id is not None:
        try:
            frame_padre.after_cancel(after_id)
        except Exception:
            pass
        frame_padre._tooltip_after_id = None

    tooltip_frame = getattr(frame_padre, "_tooltip_frame", None)
    tooltip_label = getattr(frame_padre, "_tooltip_label", None)

    # Colores según modo (activos)
    color_fondo_tooltip = configuracion.COLOR_TEXTO_URL
    color_borde_tooltip = configuracion.COLOR_TEXTO_URL
    color_texto_tooltip = configuracion.COLOR_FONDO_VENTANA

    if tooltip_frame is None or tooltip_label is None:
        tooltip_frame = ctk.CTkFrame(
            master=frame_padre,
            fg_color=color_fondo_tooltip,
            corner_radius=16,
            border_width=2,
            border_color=color_borde_tooltip
        )

        tooltip_label = ctk.CTkLabel(
            master=tooltip_frame,
            text="",
            text_color=color_texto_tooltip,
            font=("Segoe UI", 12, "bold"),
            justify="center"
        )
        tooltip_label.pack(padx=12, pady=10)

        frame_padre._tooltip_frame = tooltip_frame
        frame_padre._tooltip_label = tooltip_label

    # Actualizar estilos por si cambió el modo
    tooltip_frame.configure(
        fg_color=color_fondo_tooltip,
        border_color=color_borde_tooltip
    )
    tooltip_label.configure(
        text_color=color_texto_tooltip
    )

    tooltip_label.configure(text=mensaje)

    # Colocar dentro del frame derecho y limitar ancho
    tooltip_frame.place(relx=0.5, rely=0.06, anchor="n", relwidth=0.88)

    # Ajustar wraplength para saltos de línea (cuando el frame ya tenga tamaño real)
    def _ajustar_wrap():
        try:
            ancho = frame_padre.winfo_width()
            if ancho and ancho > 50:
                tooltip_label.configure(wraplength=int(ancho * 0.82))
        except Exception:
            pass

    frame_padre.after(0, _ajustar_wrap)

    def ocultar():
        try:
            tooltip_frame.place_forget()
        except Exception:
            pass
        frame_padre._tooltip_after_id = None

    frame_padre._tooltip_after_id = frame_padre.after(duracion_ms, ocultar)




def mostrar_tooltip_ruta_invalida(frame_padre, duracion_ms: int = 5000):
    """Muestra un tooltip con el mensaje 'Ruta invalida'."""
    mostrar_tooltip(frame_padre, "Ruta invalida", duracion_ms)




def aplicar_tema_tooltip(frame_padre):
    """
    Si hay un tooltip visible en frame_padre, reaplica colores según el modo actual.
    Esto permite que el tooltip cambie de tema al cambiar modo claro/oscuro.
    """
    if frame_padre is None:
        return

    tooltip_frame = getattr(frame_padre, "_tooltip_frame", None)
    tooltip_label = getattr(frame_padre, "_tooltip_label", None)

    if tooltip_frame is None or tooltip_label is None:
        return

    # Si no está visible, no hacemos nada
    try:
        if not tooltip_frame.winfo_ismapped():
            return
    except Exception:
        pass

    # Colores según modo (activos)
    color_fondo_tooltip = configuracion.COLOR_TEXTO_URL
    color_borde_tooltip = configuracion.COLOR_TEXTO_URL
    color_texto_tooltip = configuracion.COLOR_FONDO_VENTANA

    try:
        tooltip_frame.configure(
            fg_color=color_fondo_tooltip,
            border_color=color_borde_tooltip
        )
    except Exception:
        pass

    try:
        tooltip_label.configure(text_color=color_texto_tooltip)
    except Exception:
        pass