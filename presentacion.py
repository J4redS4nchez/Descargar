# presentacion.py
# Módulo encargado de la pantalla de presentación (splash) del programa.

import tkinter as tk
from imagenes import cargar_logo_presentacion
import configuracion
from utils.interfaz import eliminar_componente, mostrar_componente_total

class Presentacion:
    def __init__(self, ventana: tk.Tk):
        """
        Recibe la ventana principal (Tk) para dibujar la presentación
        dentro de la misma ventana.
        """
        self.ventana = ventana
        self.contenedor = None
        self.logo_tk = None

    def mostrar(self):
        """Muestra la pantalla de presentación (fondo blanco y logo centrado)."""
        # Fondo según el modo actual (claro/oscuro)
        self.contenedor = tk.Frame(self.ventana, bg=configuracion.COLOR_FONDO_VENTANA)

        mostrar_componente_total(self.contenedor)

        # Cargar logo según el modo actual (claro/oscuro)
        self.logo_tk = cargar_logo_presentacion(ancho_maximo=420)


        # El label debe tener el mismo fondo para que no se vea un parche
        etiqueta_logo = tk.Label(self.contenedor, image=self.logo_tk, bg=configuracion.COLOR_FONDO_VENTANA)

        etiqueta_logo.place(relx=0.5, rely=0.5, anchor="center")

    def ocultar(self):
        """Quita la pantalla de presentación."""
        # Usamos la herramienta de utils para destruir el contenedor
        eliminar_componente(self.contenedor)
        self.contenedor = None