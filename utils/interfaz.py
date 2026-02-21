# utils/interfaz.py

def centrar_ventana(ventana, ancho, alto):
    """Calcula y aplica la posición centrada para cualquier ventana de Tkinter."""
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def ocultar_ventana(ventana):
    """Oculta la ventana de la vista."""
    ventana.withdraw()

def mostrar_ventana_lista(ventana):
    """Fuerza la actualización de widgets y muestra la ventana final."""
    ventana.update_idletasks()
    ventana.deiconify()