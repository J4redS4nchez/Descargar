import tkinter as tk
import customtkinter as ctk
from imagenes import cargar_icono_sol_ctk, cargar_icono_luna_ctk
import configuracion




class SwitchModo:
    def __init__(
        self,
        ventana,
        y=8,
        x=-4,
        callback_cambio=None,
        color_fondo="white",
        relx=1.0,
        rely=0.0,
        anchor="ne"
    ):
        self.ventana = ventana
        self.y = y
        self.x = x
        self.callback_cambio = callback_cambio

        # Apariencia y posición del contenedor
        self.color_fondo = color_fondo
        self.relx = relx
        self.rely = rely
        self.anchor = anchor

        self.modo_oscuro = tk.BooleanVar(value=configuracion.MODO_OSCURO)

        self.contenedor = None
        self.icono = None
        self.switch = None

        #Simbolos, sol y luna
        self.imagen_sol = None
        self.imagen_luna = None


        
    def crear(self):

        #posicionar
        self.contenedor = tk.Frame(self.ventana, bg=self.color_fondo)

        # Ancho total aproximado del componente: icono + espacio + switch
        ancho_total = 6 + 18 + 34  # padding + icono + switch (aprox)

        # Tamaño fijo del contenedor para que no se recorte el switch
        alto_total = 24  # suficiente para switch_height=18 y el texto del icono
        self.contenedor.configure(width=ancho_total, height=alto_total)

        self.contenedor.place(relx=self.relx, rely=self.rely, y=self.y, x=self.x, anchor=self.anchor)

        # Evita que el Frame se encoja al contenido (para que el centrado sea real)
        self.contenedor.grid_propagate(False)

        # Configuración del grid interno
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=0)
        self.contenedor.grid_columnconfigure(1, weight=1)

        # Cargar iconos (pequeños) desde imagenes.py
        self.imagen_sol = cargar_icono_sol_ctk(ancho=14, alto=14)
        self.imagen_luna = cargar_icono_luna_ctk(ancho=14, alto=14)

        # Icono a la izquierda (imagen)
        self.icono = ctk.CTkLabel(
            master=self.contenedor,
            text="",
            image=self.imagen_sol,
            fg_color=self.color_fondo,
            bg_color=self.color_fondo
        )
        self.icono.grid(row=0, column=0, padx=(0, 6))


        # Switch pequeño estilo teléfono
        self.switch = ctk.CTkSwitch(
            master=self.contenedor,
            text="",
            variable=self.modo_oscuro,
            command=self._al_cambiar,
            bg_color=self.color_fondo,

            switch_width=34,
            switch_height=18,
            corner_radius=9,

            fg_color=configuracion.COLOR_SWITCH_RIEL_APAGADO,
            progress_color=configuracion.COLOR_SWITCH_RIEL_ENCENDIDO,
            button_color=configuracion.COLOR_SWITCH_BOTON,
            button_hover_color=configuracion.COLOR_SWITCH_BOTON_HOVER
        )


        self.switch.grid(row=0, column=1, sticky="w")


        self._actualizar_icono()

        # Asegura que la variable global quede sincronizada al iniciar
        configuracion.MODO_OSCURO = self.modo_oscuro.get()


    def _al_cambiar(self):
        self._actualizar_icono()

        configuracion.MODO_OSCURO = self.modo_oscuro.get()
        configuracion.actualizar_tema()
        
        # Guarda la preferencia para que persista al cerrar y abrir la app
        configuracion.guardar_modo_en_json()


        if self.callback_cambio is not None:
            self.callback_cambio(self.modo_oscuro.get())


    def _actualizar_icono(self):
        if self.icono is None:
            return

        # Apagado (riel gris): luna
        if not self.modo_oscuro.get():
            if self.imagen_luna is not None:
                self.icono.configure(image=self.imagen_luna)
        # Encendido (riel blanco): sol
        else:
            if self.imagen_sol is not None:
                self.icono.configure(image=self.imagen_sol)

    def esta_modo_oscuro(self):
        return self.modo_oscuro.get()



    def aplicar_tema(self, color_fondo=None):
        """
        Aplica los colores actuales de configuracion al switch.
        Si se pasa color_fondo, también actualiza el fondo del contenedor.
        """
        if color_fondo is not None:
            self.color_fondo = color_fondo

        if self.contenedor is not None:
            self.contenedor.configure(bg=self.color_fondo)

        if self.icono is not None:
            # CTkLabel acepta fg_color/bg_color
            try:
                self.icono.configure(fg_color=self.color_fondo, bg_color=self.color_fondo)
            except Exception:
                pass

        if self.switch is not None:
            self.switch.configure(
                fg_color=configuracion.COLOR_SWITCH_RIEL_APAGADO,
                progress_color=configuracion.COLOR_SWITCH_RIEL_ENCENDIDO,
                button_color=configuracion.COLOR_SWITCH_BOTON,
                button_hover_color=configuracion.COLOR_SWITCH_BOTON_HOVER,
                bg_color=self.color_fondo
            )
