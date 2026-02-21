import customtkinter as ctk
import configuracion


class FormatoTarjeta:
    """
    Componente para colocarse dentro de la tarjeta del medio (tarjeta_2).

    Contiene en una sola fila:
    - Select box (CTkComboBox)
    - Textbox (CTkEntry)
    - Botón "Examinar" (CTkButton)

    Todo centrado en el centro de la tarjeta y sin salirse (usa relwidth).
    """

    def __init__(self, tarjeta_padre, callback_cambio_formato=None):
        self.tarjeta_padre = tarjeta_padre

        # Callback opcional para notificar cuando cambia el formato
        self.callback_cambio_formato = callback_cambio_formato
        self.tarjeta_padre = tarjeta_padre

        self.contenedor_fila = None
        self.select_formato = None
        self.cuadro_ruta = None
        self.boton_examinar = None

        # Valores por defecto del select (puedes cambiarlos cuando quieras)
        self.valores_formato = [" •  •  •  •  •"," mp4", " mp3", " short"]

    def crear(self):
        """
        Crea y posiciona los elementos dentro de la tarjeta.
        """
        # Contenedor para alinear todo en una sola fila y controlar ancho total
        self.contenedor_fila = ctk.CTkFrame(
            master=self.tarjeta_padre,
            fg_color="transparent"
        )

        # Centramos el renglón a la mitad exacta de la tarjeta
        # relwidth controla que nunca se salga
        self.contenedor_fila.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.90)

        # Grid interno: [select] [textbox] [botón]
        self.contenedor_fila.grid_columnconfigure(0, weight=0)
        self.contenedor_fila.grid_columnconfigure(1, weight=1)
        self.contenedor_fila.grid_columnconfigure(2, weight=0)




        # Select box (ComboBox)
        configuracion_select = {
            "master": self.contenedor_fila,
            "values": self.valores_formato,
            "width": 90
        }

        if configuracion.COLOR_SELECT_FORMATO_FONDO is not None:
            configuracion_select["fg_color"] = configuracion.COLOR_SELECT_FORMATO_FONDO

        if configuracion.COLOR_SELECT_FORMATO_TEXTO is not None:
            configuracion_select["text_color"] = configuracion.COLOR_SELECT_FORMATO_TEXTO

        if configuracion.COLOR_SELECT_FORMATO_BORDE is not None:
            configuracion_select["border_color"] = configuracion.COLOR_SELECT_FORMATO_BORDE

        if configuracion.COLOR_SELECT_FORMATO_BOTON is not None:
            configuracion_select["button_color"] = configuracion.COLOR_SELECT_FORMATO_BOTON

        if configuracion.COLOR_SELECT_FORMATO_BOTON_HOVER is not None:
            configuracion_select["button_hover_color"] = configuracion.COLOR_SELECT_FORMATO_BOTON_HOVER

        if configuracion.COLOR_SELECT_FORMATO_DROPDOWN_FONDO is not None:
            configuracion_select["dropdown_fg_color"] = configuracion.COLOR_SELECT_FORMATO_DROPDOWN_FONDO

        if configuracion.COLOR_SELECT_FORMATO_DROPDOWN_TEXTO is not None:
            configuracion_select["dropdown_text_color"] = configuracion.COLOR_SELECT_FORMATO_DROPDOWN_TEXTO

        # Aquí ya tienes 2 colores independientes (claro/oscuro) en configuracion.py,
        # así que esto siempre debe existir (no usar None)
        configuracion_select["dropdown_hover_color"] = configuracion.COLOR_SELECT_FORMATO_DROPDOWN_HOVER

        configuracion_select["command"] = self._al_cambiar_formato
        # Crear el ComboBox (primero se crea, luego ya puedes configurar si quisieras)
        self.select_formato = ctk.CTkComboBox(**configuracion_select)
        self.select_formato.set(self.valores_formato[0])
        self.select_formato.grid(row=0, column=0, padx=(0, 10), sticky="w")





        # Textbox (Entry)
        configuracion_entry = {
            "master": self.contenedor_fila,
            "placeholder_text": "• Selecciona un archivo o escribe la ruta"
        }

        if configuracion.COLOR_TEXBOX_FORMATO_FONDO is not None:
            configuracion_entry["fg_color"] = configuracion.COLOR_TEXBOX_FORMATO_FONDO

        if configuracion.COLOR_TEXBOX_FORMATO_TEXTO is not None:
            configuracion_entry["text_color"] = configuracion.COLOR_TEXBOX_FORMATO_TEXTO

        if configuracion.COLOR_TEXBOX_FORMATO_PLACEHOLDER is not None:
            configuracion_entry["placeholder_text_color"] = configuracion.COLOR_TEXBOX_FORMATO_PLACEHOLDER

        if configuracion.COLOR_TEXBOX_FORMATO_BORDE is not None:
            configuracion_entry["border_color"] = configuracion.COLOR_TEXBOX_FORMATO_BORDE

        self.cuadro_ruta = ctk.CTkEntry(**configuracion_entry)
        self.cuadro_ruta.grid(row=0, column=1, sticky="ew")


        # Asegurar que el textbox reciba el foco al hacer click (para permitir escribir/borrar/pegar)
        self.cuadro_ruta.bind("<Button-1>", lambda evento: self.cuadro_ruta.focus_set())


        # Colocar por defecto la ruta de Descargas en el textbox
        from funcionamiento.examinar import obtener_ruta_descargas
        self.establecer_ruta(obtener_ruta_descargas())


        # Asegurar que el usuario pueda editar la ruta manualmente
        self.cuadro_ruta.configure(state="normal")


        # Asegurar edición real en el Entry interno de CustomTkinter
        # (a veces el wrapper se ve editable pero el Entry interno queda bloqueado)
        try:
            self.cuadro_ruta._entry.configure(state="normal")
        except Exception:
            pass

        # Asegurar que el foco caiga en el Entry interno al hacer click
        try:
            self.cuadro_ruta._entry.bind("<Button-1>", lambda evento: self.cuadro_ruta._entry.focus_set())
        except Exception:
            pass

        # Botón Examinar


        self.boton_examinar = ctk.CTkButton(
            master=self.contenedor_fila,
            text="Examinar",
            width=110,
            height=32,
            corner_radius=10,
            fg_color=configuracion.COLOR_BOTON_EXAMINAR_FONDO,
            hover_color=configuracion.COLOR_BOTON_EXAMINAR_HOVER,
            text_color=configuracion.COLOR_BOTON_EXAMINAR_TEXTO,
            command=self._al_presionar_examinar
        )
        self.boton_examinar.grid(row=0, column=2, padx=(10, 0), sticky="e")

        # Aplicar tema inicial (por si arranca en modo oscuro)
        self.aplicar_tema()
        # Colocar el foco inicial en el textbox para que el usuario pueda empezar a escribir de inmediato
        # Colocar foco inicial real en el Entry interno
        try:
            self.cuadro_ruta._entry.focus_set()
        except Exception:
            self.cuadro_ruta.focus_set()





    def aplicar_tema(self):
        """
        Aplica colores del tema actual a select, textbox y botón.
        """
        if self.cuadro_ruta is not None:
            if configuracion.COLOR_TEXBOX_FORMATO_FONDO is not None:
                self.cuadro_ruta.configure(fg_color=configuracion.COLOR_TEXBOX_FORMATO_FONDO)

            if configuracion.COLOR_TEXBOX_FORMATO_TEXTO is not None:
                self.cuadro_ruta.configure(text_color=configuracion.COLOR_TEXBOX_FORMATO_TEXTO)

            if configuracion.COLOR_TEXBOX_FORMATO_PLACEHOLDER is not None:
                self.cuadro_ruta.configure(placeholder_text_color=configuracion.COLOR_TEXBOX_FORMATO_PLACEHOLDER)

            if configuracion.COLOR_TEXBOX_FORMATO_BORDE is not None:
                self.cuadro_ruta.configure(border_color=configuracion.COLOR_TEXBOX_FORMATO_BORDE)


        # Aplica el tema al select, pero solo manda dropdown_hover_color si NO es None
        if self.select_formato is not None:
            configuracion_select = {
                "fg_color": configuracion.COLOR_SELECT_FORMATO_FONDO,
                "text_color": configuracion.COLOR_SELECT_FORMATO_TEXTO,
                "border_color": configuracion.COLOR_SELECT_FORMATO_BORDE,
                "button_color": configuracion.COLOR_SELECT_FORMATO_BOTON,
                "button_hover_color": configuracion.COLOR_SELECT_FORMATO_BOTON_HOVER,
                "dropdown_fg_color": configuracion.COLOR_SELECT_FORMATO_DROPDOWN_FONDO,
                "dropdown_text_color": configuracion.COLOR_SELECT_FORMATO_DROPDOWN_TEXTO
            }

            # Si en modo oscuro es None, no lo mandamos y se queda el hover por defecto
            if configuracion.COLOR_SELECT_FORMATO_DROPDOWN_HOVER is not None:
                configuracion_select["dropdown_hover_color"] = configuracion.COLOR_SELECT_FORMATO_DROPDOWN_HOVER

            self.select_formato.configure(**configuracion_select)




        if self.boton_examinar is not None:
            self.boton_examinar.configure(
                fg_color=configuracion.COLOR_BOTON_EXAMINAR_FONDO,
                hover_color=configuracion.COLOR_BOTON_EXAMINAR_HOVER,
                text_color=configuracion.COLOR_BOTON_EXAMINAR_TEXTO
            )

    def obtener_formato(self) -> str:
        """
        Devuelve el formato seleccionado del select.
        """
        if self.select_formato is None:
            return ""
        return str(self.select_formato.get())

    def obtener_ruta(self) -> str:
        """
        Devuelve el texto del textbox.
        """
        if self.cuadro_ruta is None:
            return ""
        return self.cuadro_ruta.get()


    def establecer_ruta(self, texto: str):
        """
        Coloca un texto en el textbox de ruta.

        Nota:
        - Si el Entry está en estado deshabilitado o readonly, se cambia temporalmente a normal
        para poder insertar el texto, y luego se regresa al estado anterior.
        """
        if self.cuadro_ruta is None:
            return

        # Guardar el estado actual por si estaba deshabilitado/readonly
        try:
            estado_anterior = self.cuadro_ruta.cget("state")
        except Exception:
            estado_anterior = "normal"

        # Forzar a normal para poder escribir
        try:
            self.cuadro_ruta.configure(state="normal")
        except Exception:
            pass

        self.cuadro_ruta.delete(0, "end")
        self.cuadro_ruta.insert(0, texto)

        # Regresar al estado anterior (si aplica)
        try:
            self.cuadro_ruta.configure(state=estado_anterior)
        except Exception:
            pass


    def _al_presionar_examinar(self):
        """
        Acción del botón Examinar.
        Abre el selector de carpetas y coloca la ruta seleccionada en el textbox.
        """
        # Import local para no cargar módulos innecesarios al iniciar
        from funcionamiento.examinar import seleccionar_carpeta_guardado

        # Ventana principal (CTk/Tk) para asociar correctamente el diálogo
        ventana_principal = None
        try:
            ventana_principal = self.tarjeta_padre.winfo_toplevel()
        except Exception:
            ventana_principal = None

        # Usar la ruta actual del textbox como carpeta inicial si existe
        ruta_actual = self.obtener_ruta().strip()
        ruta_seleccionada = seleccionar_carpeta_guardado(
            ventana_padre=ventana_principal,
            ruta_inicial=ruta_actual
        )

        # Si el usuario canceló, no hacemos nada
        if not ruta_seleccionada:
            return

        # Colocar la ruta elegida en el textbox
        self.establecer_ruta(ruta_seleccionada)

        # Asegurar foco para permitir seguir editando si quiere
        try:
            self.cuadro_ruta._entry.focus_set()
        except Exception:
            try:
                self.cuadro_ruta.focus_set()
            except Exception:
                pass




    def _al_cambiar_formato(self, _valor_seleccionado=None):
        """
        Se ejecuta cuando el usuario cambia la opción del ComboBox.
        Notifica al callback (si existe) el formato actual.
        """
        if callable(self.callback_cambio_formato):
            try:
                self.callback_cambio_formato(self.obtener_formato())
            except Exception:
                pass