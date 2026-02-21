# funcionamiento/descargar.py

def actualizar_visibilidad_boton_descargar(boton_descargar, tarjeta_padre, visible: bool, margen: int = 12):
    """
    Muestra u oculta el botón de descargar sin destruirlo.

    Parámetros:
    - boton_descargar: botón (CTkButton) ya creado.
    - tarjeta_padre: frame/tarjeta donde se posiciona el botón.
    - visible: True para mostrar, False para ocultar.
    - margen: separación con respecto a la esquina superior derecha.
    """
    if boton_descargar is None or tarjeta_padre is None:
        return

    if not bool(visible):
        # Oculta el botón sin destruirlo
        try:
            boton_descargar.place_forget()
        except Exception:
            pass
        return

    # Mostrar: colocarlo en la esquina superior derecha
    try:
        tarjeta_padre.update_idletasks()
        ancho_boton = boton_descargar.winfo_reqwidth()

        boton_descargar.place(
            x=tarjeta_padre.winfo_width() - ancho_boton - margen,
            y=margen
        )
    except Exception:
        # Si algo falla al recalcular, no rompemos la app
        pass