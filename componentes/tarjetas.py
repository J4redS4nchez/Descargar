import customtkinter as ctk
from imagenes import cargar_icono_luz_ctk, cargar_icono_oscuro_ctk
from componentes.switch_MODO import SwitchModo
import configuracion
from componentes.URL import URLTarjeta
from componentes.progreso import ProgresoTarjeta
from componentes.formato import FormatoTarjeta



class TarjetasLayout:
    """
    Crea y posiciona 4 tarjetas:
    - 3 tarjetas apiladas en la columna izquierda
    - 1 tarjeta alta en la columna derecha (ocupa las 3 filas)
    """

    def __init__(self, ventana, color_tarjeta=None):
        self.ventana = ventana
        self.color_tarjeta = color_tarjeta if color_tarjeta is not None else configuracion.COLOR_TARJETAS

        self.switch_modo = None

        self.contenedor = None
        self.tarjeta_1 = None
        self.tarjeta_2 = None
        self.tarjeta_3 = None
        self.tarjeta_4 = None
        # Referencias para evitar que la imagen se "pierda" por el garbage collector
        self.imagen_icono = None
        self.etiqueta_icono = None
        self.ancho_icono = 170
        self.alto_icono = 230
        self.componente_url = None
        self.componente_progreso = None
        self.componente_formato = None





    def crear(self):
        """Crea el layout de tarjetas en la ventana."""
        # Contenedor principal de las tarjetas
        self.contenedor = ctk.CTkFrame(master=self.ventana, fg_color=configuracion.COLOR_FONDO_VENTANA, corner_radius=0)

        self.contenedor.pack(fill="both", expand=True, padx=18, pady=18)

        # Grid: 2 columnas, 3 filas
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_rowconfigure(1, weight=1)
        self.contenedor.grid_rowconfigure(2, weight=1)

        self.contenedor.grid_columnconfigure(0, weight=9)
        self.contenedor.grid_columnconfigure(1, weight=1)

        # Estilo común de tarjetas
        estilo_tarjeta = {
            "fg_color": configuracion.COLOR_TARJETAS,
            "corner_radius": 22,
            "border_width": 0
        }

        # Tarjetas izquierdas (3 filas)
        self.tarjeta_1 = ctk.CTkFrame(master=self.contenedor, **estilo_tarjeta)
        self.tarjeta_2 = ctk.CTkFrame(master=self.contenedor, **estilo_tarjeta)
        self.tarjeta_3 = ctk.CTkFrame(master=self.contenedor, **estilo_tarjeta)

        # Tarjeta derecha (alta, ocupa 3 filas)
        self.tarjeta_4 = ctk.CTkFrame(master=self.contenedor, **estilo_tarjeta)

        # Posicionamiento (similar a tu dibujo)
        separacion = 18

        self.tarjeta_1.grid(row=0, column=0, sticky="nsew", padx=(0, separacion), pady=(0, separacion))
        self.tarjeta_2.grid(row=1, column=0, sticky="nsew", padx=(0, separacion), pady=(0, separacion))
        self.tarjeta_3.grid(row=2, column=0, sticky="nsew", padx=(0, separacion), pady=(0, 0))

        self.tarjeta_4.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=(0, 0), pady=(0, 0))


        # Contenido de la tarjeta 1 (URL)
        self.componente_url = URLTarjeta(self.tarjeta_1)
        self.componente_url.crear()


        # Contenido de la tarjeta 2 (formato + ruta + examinar)
        self.componente_formato = FormatoTarjeta(
            self.tarjeta_2,
            callback_cambio_formato=self._al_cambiar_formato,
            callback_cambio_ruta=self._al_cambiar_ruta
        )
        self.componente_formato.crear()


        # Contenido de la tarjeta 3 (barra de progreso)
        self.componente_progreso = ProgresoTarjeta(self.tarjeta_3)
        self.componente_progreso.crear()

        # Estado inicial del botón descargar según el formato actual
        self._actualizar_visibilidad_descarga()

        # Icono inicial según el modo actual
        if configuracion.MODO_OSCURO:
            self.imagen_icono = cargar_icono_oscuro_ctk(ancho=self.ancho_icono, alto=self.alto_icono)
        else:
            self.imagen_icono = cargar_icono_luz_ctk(ancho=self.ancho_icono, alto=self.alto_icono)


        self.etiqueta_icono = ctk.CTkLabel(
            master=self.tarjeta_4,
            text="",
            image=self.imagen_icono,
            fg_color=self.color_tarjeta
        )
        self.etiqueta_icono.place(relx=0.5, rely=0.5, anchor="center")

        # Switch dentro de la tarjeta derecha, abajo con margen
        self.switch_modo = SwitchModo(
            self.tarjeta_4,
            callback_cambio=self._al_cambiar_modo,
            color_fondo=configuracion.COLOR_TARJETAS,
            relx=0.5,   # centrado horizontal
            rely=1.0,   # pegado hacia abajo
            anchor="s", # ancla abajo-centro
            x=0,
            y=-14       # margen hacia arriba para que no choque con el borde
        )
        self.switch_modo.crear()
        self.aplicar_tema()


    def aplicar_tema(self):
        """Aplica los colores actuales desde configuracion a ventana y tarjetas."""
        # Fondo de la ventana
        try:
            self.ventana.configure(bg=configuracion.COLOR_FONDO_VENTANA)
        except Exception:
            pass

        # Fondo del contenedor
        if self.contenedor is not None:
            self.contenedor.configure(fg_color=configuracion.COLOR_FONDO_VENTANA)

        # Tarjetas
        for tarjeta in [self.tarjeta_1, self.tarjeta_2, self.tarjeta_3, self.tarjeta_4]:
            if tarjeta is not None:
                tarjeta.configure(fg_color=configuracion.COLOR_TARJETAS)

        # Etiqueta del logo (para que no se vea “parchada”)
        if self.etiqueta_icono is not None:
            self.etiqueta_icono.configure(fg_color=configuracion.COLOR_TARJETAS)
        

        # Cambiar icono según el modo
        if self.etiqueta_icono is not None:
            if configuracion.MODO_OSCURO:
                self.imagen_icono = cargar_icono_oscuro_ctk(ancho=self.ancho_icono, alto=self.alto_icono)
            else:
                self.imagen_icono = cargar_icono_luz_ctk(ancho=self.ancho_icono, alto=self.alto_icono)

            self.etiqueta_icono.configure(image=self.imagen_icono)

        # Aplicar tema al switch dentro de la tarjeta derecha
        if self.switch_modo is not None:
            self.switch_modo.aplicar_tema(color_fondo=configuracion.COLOR_TARJETAS)

        # Actualiza el contenido de la tarjeta URL (icono de basura)
        if hasattr(self, "componente_url") and self.componente_url is not None:
            self.componente_url.aplicar_tema()


        # Actualiza la barra de progreso (fondo integrado a la tarjeta)
        if hasattr(self, "componente_progreso") and self.componente_progreso is not None:
            self.componente_progreso.aplicar_tema()


        # Actualiza el contenido de la tarjeta Formato
        if hasattr(self, "componente_formato") and self.componente_formato is not None:
            self.componente_formato.aplicar_tema()


    def _al_cambiar_formato(self, _formato_actual: str):
        """
        Se llama cuando el usuario cambia el formato en el ComboBox.
        """
        self._actualizar_visibilidad_descarga()



    def _al_cambiar_ruta(self, _ruta_actual: str):
        """
        Se llama cuando el usuario cambia la ruta en el textbox.
        """
        self._actualizar_visibilidad_descarga()



    def _actualizar_visibilidad_descarga(self):
        """
        Oculta el botón descargar si:
        - el formato es el placeholder " •  •  •  •  •"
        O
        - la ruta está vacía

        Solo lo muestra si:
        - NO es placeholder
        Y
        - la ruta NO está vacía
        """
        if self.componente_formato is None or self.componente_progreso is None:
            return

        formato_actual = self.componente_formato.obtener_formato()
        placeholder = self.componente_formato.valores_formato[0]
        es_placeholder = (str(formato_actual).strip() == str(placeholder).strip())

        ruta_actual = str(self.componente_formato.obtener_ruta()).strip()
        ruta_vacia = (ruta_actual == "")

        mostrar = (not es_placeholder) and (not ruta_vacia)

        self.componente_progreso.establecer_visibilidad_boton_descargar(mostrar)


    def _al_cambiar_modo(self, _esta_oscuro):
        """Se llama cuando cambia el switch."""
        self.aplicar_tema()
