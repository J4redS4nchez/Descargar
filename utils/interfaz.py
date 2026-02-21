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



def mostrar_componente_total(componente):
    """Muestra un componente ocupando todo el espacio disponible (fill both)."""
    if componente is not None:
        componente.pack(fill="both", expand=True)

def eliminar_componente(componente):
    """Destruye un widget de forma segura y limpia."""
    if componente is not None:
        componente.destroy()


def configurar_columnas_grid(contenedor, pesos):
    """Configura el peso de múltiples columnas de una sola vez."""
    for i, peso in enumerate(pesos):
        contenedor.grid_columnconfigure(i, weight=peso)

def crear_etiqueta_estandar(contenedor, texto, color_fondo, fuente=("Arial", 12)):
    """Crea una etiqueta con el estilo común del proyecto."""
    return tk.Label(contenedor, text=texto, bg=color_fondo, font=fuente)


# utils/interfaz.py

def configurar_filas_grid(contenedor, pesos):
    """Configura el peso de múltiples filas de una sola vez."""
    for i, peso in enumerate(pesos):
        contenedor.grid_rowconfigure(i, weight=peso)

def configurar_columnas_grid(contenedor, pesos):
    """Configura el peso de múltiples columnas de una sola vez."""
    for i, peso in enumerate(pesos):
        contenedor.grid_columnconfigure(i, weight=peso)