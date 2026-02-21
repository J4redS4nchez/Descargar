import customtkinter as ctk
import configuracion
import tkinter as tk

from imagenes import (
    cargar_icono_basura_claro_ctk,
    cargar_icono_basura_oscuro_ctk,
    cargar_icono_desplegar_claro_ctk,
    cargar_icono_desplegar_oscuro_ctk
)


from PIL import Image
from imagenes import obtener_ruta_icono_desplegar_claro, obtener_ruta_icono_desplegar_oscuro



class URLTarjeta:
    """
    Componente para la tarjeta 1.
    Muestra el texto 'URL:' y un cuadro de texto para escribir.
    Todo queda centrado dentro de la tarjeta.
    """

    def __init__(self, tarjeta_padre, callback_cambio_url=None):
        self.tarjeta_padre = tarjeta_padre

        # Callback opcional para notificar cuando cambia la URL (principal o renglones extra)
        self.callback_cambio_url = callback_cambio_url

        self.etiqueta_url = None
        self.cuadro_url = None
        self.boton_borrar = None
        self.icono_basura = None
        self.icono_basura_normal = None
        self.icono_basura_grande = None
        self.boton_desplegar = None
        self.icono_desplegar_normal = None
        self.icono_desplegar_grande = None
        self.separacion_entre_renglones = 6
        self.placeholder_url_normal = "• Pega aquí la URL"
        self.placeholder_url_lista = "• Pega aquí las URLs"

        # Contenedor y renglones adicionales (para desplegar 5 renglones en total)
        self.contenedor_renglones = None
        self.renglones_extra = []


        # Botones "x" por renglón (solo visibles cuando la lista está desplegada)
        self.boton_x_principal = None
        self.botones_x_extra = []
        self.contenedor_entry_principal = None
        self.contenedores_renglones_extra = []



        self.altura_entry = None

        # Estado del botón desplegar
        self.desplegado = False


        # Ángulo actual del icono (270 = abajo, 90 = arriba)
        self.angulo_desplegar = 0

        # Imagen base (PIL) del icono desplegar, se recarga con el tema
        self.imagen_desplegar_base = None



    def crear(self):
        """
        Crea y posiciona los elementos dentro de la tarjeta.
        """
        # Texto "URL:" centrado (un poco arriba del centro)
        self.etiqueta_url = ctk.CTkLabel(
            master=self.tarjeta_padre,
            text="URL",
            font=("Arial", 18, "bold"),
            text_color=configuracion.COLOR_TEXTO_URL
        )
        self.etiqueta_url.place(relx=0.5, rely=0.40, anchor="center")

        # Textbox (para escribir) centrado (un poco abajo del centro)
        # Usamos CTkEntry porque es ideal para una URL (una sola línea).
        # Contenedor para alinear el Entry y el botón en una sola fila
        contenedor_fila = ctk.CTkFrame(
            master=self.tarjeta_padre,
            fg_color="transparent"
        )
        contenedor_fila.place(relx=0.5, rely=0.60, anchor="center", relwidth=0.88)

        # Configuración del grid para que el Entry use casi todo el ancho
        # 3 columnas: [desplegar] [entry] [basura]
        contenedor_fila.grid_columnconfigure(0, weight=0)
        contenedor_fila.grid_columnconfigure(1, weight=1)
        contenedor_fila.grid_columnconfigure(2, weight=0)


        # Contenedor del entry principal (se usa para colocar la "x" encima del textbox)
        self.contenedor_entry_principal = ctk.CTkFrame(
            master=contenedor_fila,
            fg_color="transparent"
        )
        self.contenedor_entry_principal.grid(row=0, column=1, sticky="ew", padx=(8, 8))
        self.contenedor_entry_principal.grid_columnconfigure(0, weight=1)



        # Configuración opcional de colores del textbox (si están en None, no se fuerzan)
        configuracion_entry = {
            "master": self.contenedor_entry_principal,
            "placeholder_text": "• Pega aquí la URL"
        }





        if configuracion.COLOR_TEXBOX_URL_FONDO is not None:
            configuracion_entry["fg_color"] = configuracion.COLOR_TEXBOX_URL_FONDO

        if configuracion.COLOR_TEXBOX_URL_TEXTO is not None:
            configuracion_entry["text_color"] = configuracion.COLOR_TEXBOX_URL_TEXTO

        if configuracion.COLOR_TEXBOX_URL_PLACEHOLDER is not None:
            configuracion_entry["placeholder_text_color"] = configuracion.COLOR_TEXBOX_URL_PLACEHOLDER

        if configuracion.COLOR_TEXBOX_URL_BORDE is not None:
            configuracion_entry["border_color"] = configuracion.COLOR_TEXBOX_URL_BORDE

        self.cuadro_url = ctk.CTkEntry(**configuracion_entry)


        # El entry principal ocupa todo el ancho de su contenedor
        self.cuadro_url.grid(row=0, column=0, sticky="ew")


        # Detectar cuando el usuario escribe o borra en el cuadro URL principal
        self.cuadro_url.bind("<KeyRelease>", self._al_cambiar_url)


        # Guardar altura del entry principal para igualarla en los renglones extra
        self.altura_entry = self.cuadro_url.cget("height")



        # Botón "x" del renglón principal:
        # Se pinta igual que el textbox para que no se vea el cuadro, solo la "x".
        color_fondo_x = configuracion.COLOR_TEXBOX_URL_FONDO
        if color_fondo_x is None:
            # Si no hay color forzado en configuración, tomamos el color real del entry.
            color_fondo_x = self.cuadro_url.cget("fg_color")

        self.boton_x_principal = ctk.CTkButton(
            master=self.contenedor_entry_principal,
            text="x",
            width=22,
            height=22,
            command=lambda: self._borrar_entry(self.cuadro_url),
            fg_color=color_fondo_x,
            bg_color="transparent",
            text_color=configuracion.COLOR_BOTON_X_TEXTO,
            hover=False,
            border_width=0,
            corner_radius=0
        )

        # Se oculta al inicio (solo aparece al desplegar la lista).
        self.boton_x_principal.place_forget()

        # El contenedor de renglones extra debe vivir en la ventana raíz para poder
        # pasar por encima de otras tarjetas (evitar que lo tapen).
        self.ventana_raiz = self.tarjeta_padre.winfo_toplevel()

        # Hacemos que el fondo del contenedor sea el mismo de la tarjeta,
        # así los espacios entre renglones se ven como separación real.
        color_fondo_tarjeta = self.tarjeta_padre.cget("fg_color")

        # Importante:
        # Los renglones extra se crearán bajo demanda (lazy) la primera vez que el usuario despliegue.
        # Esto reduce el trabajo del arranque y hace que la ventana principal aparezca más rápido.
        self.contenedor_renglones = None


        # Registrar un manejador global para detectar clicks fuera del cuadro URL
        self._registrar_click_fuera_del_cuadro()


        # Cargar iconos (normal y grande) para efecto hover
        self._cargar_iconos_basura()



        # Cargar iconos (normal y grande) para efecto hover del botón desplegar
        self._cargar_iconos_desplegar()


        # Botón de desplegar (solo icono, sin rectángulo)
        # Por el momento no tiene funcionalidad.
        self.boton_desplegar = ctk.CTkButton(
            master=contenedor_fila,
            text="",
            width=36,
            height=32,
            image=self.icono_desplegar_normal,
            command=self._al_presionar_desplegar,
            fg_color="transparent",
            bg_color="transparent",
            hover=False,
            border_width=0,
            corner_radius=0
        )
        self.boton_desplegar.grid(row=0, column=0)

        # Eventos hover (entrar/salir)
        self.boton_desplegar.bind("<Enter>", self._al_entrar_boton_desplegar)
        self.boton_desplegar.bind("<Leave>", self._al_salir_boton_desplegar)


        # Botón de borrar (solo icono, sin rectángulo)
        self.boton_borrar = ctk.CTkButton(
            master=contenedor_fila,
            text="",
            width=36,
            height=32,
            image=self.icono_basura_normal,
            command=self._borrar_texto,
            fg_color="transparent",
            bg_color="transparent",
            hover=False,
            border_width=0,
            corner_radius=0
        )
        self.boton_borrar.grid(row=0, column=2)

        # Eventos hover (entrar/salir)
        self.boton_borrar.bind("<Enter>", self._al_entrar_boton_basura)
        self.boton_borrar.bind("<Leave>", self._al_salir_boton_basura)




    def obtener_url(self) -> str:
        """
        Devuelve el texto actual del cuadro URL.
        """
        if self.cuadro_url is None:
            return ""
        return self.cuadro_url.get()

    def establecer_url(self, texto: str):
        """
        Coloca un texto en el cuadro URL.
        """
        if self.cuadro_url is None:
            return
        self.cuadro_url.delete(0, "end")
        self.cuadro_url.insert(0, texto)



    def _notificar_cambio_url(self):
        """
        Notifica al callback (si existe) que algo cambió en la sección URL.
        Sirve para que el layout decida si muestra u oculta el botón descargar.
        """
        if callable(getattr(self, "callback_cambio_url", None)):
            try:
                self.callback_cambio_url()
            except Exception:
                pass


    def _al_cambiar_url(self, _evento=None):
        """
        Se ejecuta cuando el usuario escribe o borra en algún Entry de URL.
        """
        self._notificar_cambio_url()




    def _borrar_texto(self):
        """
        Borra el contenido del textbox.

        - Si la lista NO está desplegada: borra solo el renglón principal.
        - Si la lista SÍ está desplegada: borra el renglón principal y todos los renglones extra.

        Después de borrar:
        - Reaplica los placeholder_text para que se vean desde la primera vez.
        - Quita el foco de los Entries para que el placeholder se renderice inmediatamente.
        """
        if self.cuadro_url is None:
            return

        # 1) Limpiar renglón principal
        self.cuadro_url.delete(0, "end")

        # Reaplicar placeholder del renglón principal según el estado actual
        placeholder_principal = self.placeholder_url_lista if self.desplegado else self.placeholder_url_normal
        self.cuadro_url.configure(placeholder_text=placeholder_principal)

        # 2) Si está desplegado, limpiar también los renglones extra
        if self.desplegado:
            for entry_extra in self.renglones_extra:
                if entry_extra is not None:
                    entry_extra.delete(0, "end")
                    # Reaplicar placeholder del renglón extra
                    entry_extra.configure(placeholder_text="•")

        # 3) Forzar refresco visual del placeholder:
        # Quitamos el foco de los entries (después del click del botón)
        try:
            ventana_raiz = self.tarjeta_padre.winfo_toplevel()
            ventana_raiz.after(10, lambda: ventana_raiz.focus_set())
        except Exception:
            pass

        # Notificar que la URL cambió (para actualizar visibilidad del botón descargar)
        self._notificar_cambio_url()



    def _borrar_entry(self, entry):
        """
        Borra el contenido de un Entry específico y restaura su placeholder desde la primera vez.

        Nota: CustomTkinter a veces no vuelve a dibujar el placeholder inmediatamente después de delete(),
        por eso aquí se reaplica el placeholder y se quita el foco para forzar el refresco visual.
        """
        if entry is None:
            return

        # 1) Borrar contenido
        entry.delete(0, "end")

        # 2) Reaplicar placeholder correcto
        if entry == self.cuadro_url:
            # Si es el renglón principal, depende si está desplegado o no
            placeholder = self.placeholder_url_lista if self.desplegado else self.placeholder_url_normal
            entry.configure(placeholder_text=placeholder)
        else:
            # Si es un renglón extra
            entry.configure(placeholder_text="•")

        # 3) Forzar refresco visual del placeholder quitando el foco
        try:
            ventana_raiz = self.tarjeta_padre.winfo_toplevel()
            ventana_raiz.after(10, lambda: ventana_raiz.focus_set())
        except Exception:
            pass


        # Notificar que la URL cambió (para actualizar visibilidad del botón descargar)
        self._notificar_cambio_url()


    def _mostrar_boton_x_principal(self):
        """
        Muestra la "x" del renglón principal cuando la lista está desplegada.
        """
        if self.boton_x_principal is None or self.cuadro_url is None:
            return

        # Posicionar la "x" encima del entry (dentro del contenedor del entry)
        self.boton_x_principal.place(relx=1.0, rely=0.5, anchor="e", x=-6)


    def _ocultar_boton_x_principal(self):
        """
        Oculta la "x" del renglón principal cuando la lista no está desplegada.
        """
        if self.boton_x_principal is None:
            return
        self.boton_x_principal.place_forget()




    def aplicar_tema(self):
        """
        Recarga los iconos (normal y grande) según el modo actual
        y deja el botón en estado normal.
        """
        # Recargar iconos del botón desplegar para el modo actual
        if self.boton_desplegar is not None:
            self._cargar_iconos_desplegar()
            self.boton_desplegar.configure(image=self.icono_desplegar_normal)



        if self.boton_borrar is None:
            return


        # Recargar iconos para el modo actual
        self._cargar_iconos_basura()

        # Forzar el estado visual a "normal" (sin hover)
        self.boton_borrar.configure(image=self.icono_basura_normal)

        # Actualiza color del texto "URL:" según el modo actual
        if self.etiqueta_url is not None:
            self.etiqueta_url.configure(text_color=configuracion.COLOR_TEXTO_URL)

        # Actualiza colores del textbox (si se configuraron)
        if self.cuadro_url is not None:


            # Mantener la "x" del renglón principal del mismo color que el textbox
            color_fondo_x = configuracion.COLOR_TEXBOX_URL_FONDO
            if color_fondo_x is None and self.cuadro_url is not None:
                color_fondo_x = self.cuadro_url.cget("fg_color")

            if self.boton_x_principal is not None:
                self.boton_x_principal.configure(
                    fg_color=color_fondo_x,
                    bg_color="transparent",
                    text_color=configuracion.COLOR_BOTON_X_TEXTO
                )

            if configuracion.COLOR_TEXBOX_URL_FONDO is not None:
                self.cuadro_url.configure(fg_color=configuracion.COLOR_TEXBOX_URL_FONDO)

            if configuracion.COLOR_TEXBOX_URL_TEXTO is not None:
                self.cuadro_url.configure(text_color=configuracion.COLOR_TEXBOX_URL_TEXTO)

            if configuracion.COLOR_TEXBOX_URL_PLACEHOLDER is not None:
                self.cuadro_url.configure(placeholder_text_color=configuracion.COLOR_TEXBOX_URL_PLACEHOLDER)

            if configuracion.COLOR_TEXBOX_URL_BORDE is not None:
                self.cuadro_url.configure(border_color=configuracion.COLOR_TEXBOX_URL_BORDE)


        # Mantener el fondo del contenedor de renglones igual al de la tarjeta
        if self.contenedor_renglones is not None:
            self.contenedor_renglones.configure(fg_color=self.tarjeta_padre.cget("fg_color"))

            # Aplicar tema a renglones extra si existen
            for entry_extra, boton_x in zip(self.renglones_extra, self.botones_x_extra):
                if configuracion.COLOR_TEXBOX_URL_FONDO is not None:
                    entry_extra.configure(fg_color=configuracion.COLOR_TEXBOX_URL_FONDO)

                if configuracion.COLOR_TEXBOX_URL_TEXTO is not None:
                    entry_extra.configure(text_color=configuracion.COLOR_TEXBOX_URL_TEXTO)

                if configuracion.COLOR_TEXBOX_URL_PLACEHOLDER is not None:
                    entry_extra.configure(placeholder_text_color=configuracion.COLOR_TEXBOX_URL_PLACEHOLDER)

                if configuracion.COLOR_TEXBOX_URL_BORDE is not None:
                    entry_extra.configure(border_color=configuracion.COLOR_TEXBOX_URL_BORDE)


                # Mantener las "x" extra del mismo color que su textbox
                color_fondo_x = configuracion.COLOR_TEXBOX_URL_FONDO
                if color_fondo_x is None:
                    color_fondo_x = entry_extra.cget("fg_color")

                if boton_x is not None:
                    boton_x.configure(
                        fg_color=color_fondo_x,
                        bg_color="transparent",
                        text_color=configuracion.COLOR_BOTON_X_TEXTO
                    )





    def _cargar_iconos_basura(self):
        """
        Carga dos versiones del icono: normal y grande (hover) según el modo actual.
        """
        if configuracion.MODO_OSCURO:
            self.icono_basura_normal = cargar_icono_basura_oscuro_ctk(ancho=22, alto=22)
            self.icono_basura_grande = cargar_icono_basura_oscuro_ctk(ancho=26, alto=26)
        else:
            self.icono_basura_normal = cargar_icono_basura_claro_ctk(ancho=22, alto=22)
            self.icono_basura_grande = cargar_icono_basura_claro_ctk(ancho=26, alto=26)


    def _al_entrar_boton_basura(self, evento=None):

        """
        Al pasar el cursor sobre el botón, agranda el icono.
        """
        if self.boton_borrar is None or self.icono_basura_grande is None:
            return
        self.boton_borrar.configure(image=self.icono_basura_grande)

    def _al_salir_boton_basura(self, evento=None):
        """
        Al quitar el cursor del botón, regresa el icono a su tamaño normal.
        """
        if self.boton_borrar is None or self.icono_basura_normal is None:
            return
        self.boton_borrar.configure(image=self.icono_basura_normal)



    def _registrar_click_fuera_del_cuadro(self):
        """
        Registra un evento de click en la ventana para quitar el foco del cuadro URL
        cuando el usuario hace click fuera de él. Esto permite que vuelva a mostrarse
        el placeholder si el cuadro está vacío.
        """
        # Guardamos referencia a la ventana principal (Toplevel/raíz)
        self.ventana_raiz = self.tarjeta_padre.winfo_toplevel()

        # add="+" para no reemplazar otros binds que pudieras tener
        self.ventana_raiz.bind("<Button-1>", self._al_click_en_ventana, add="+")

    def _al_click_en_ventana(self, evento):
        """
        Si se hace click fuera del CTkEntry (y fuera del botón de borrar),
        quita el foco del cuadro URL para que reaparezca el placeholder.
        """
        if self.cuadro_url is None:
            return

        widget_clickeado = evento.widget

        # Si el click fue sobre cualquier cuadro de texto (Entry), no robamos el foco.
        # Esto permite que otros componentes (por ejemplo el textbox de ruta) funcionen independiente.
        try:
            if isinstance(widget_clickeado, (ctk.CTkEntry, tk.Entry)):
                return
        except Exception:
            pass

        # CTkEntry usa un Entry interno; si el click cae en un hijo interno, detectarlo subiendo por los masters.
        if self._es_descendiente_de(widget_clickeado, getattr(self.cuadro_url, "_entry", None)):
            return

        # CTkEntry usa un widget interno de tkinter; lo consideramos también
        entry_interno = getattr(self.cuadro_url, "_entry", None)

        # Si el click fue dentro del cuadro (o su widget interno) o en el botón de borrar, no hacemos nada
        widgets_permitidos = [self.cuadro_url, entry_interno, self.boton_borrar, self.boton_desplegar]
        widgets_permitidos.extend(self.renglones_extra)

        if widget_clickeado in tuple(widgets_permitidos):
            return


        for entry_extra in self.renglones_extra:
            if self._es_descendiente_de(widget_clickeado, entry_extra):
                return

        # Si el click fue en algún hijo del cuadro o del botón, tampoco hacemos nada
        if self._es_descendiente_de(widget_clickeado, self.cuadro_url):
            return
        if self._es_descendiente_de(widget_clickeado, self.boton_borrar):
            return

        # Si cualquier entry está vacío, quitamos foco para que su placeholder vuelva a mostrarse
        if self.cuadro_url is not None and self.cuadro_url.get().strip() == "":
            self.ventana_raiz.focus_set()
            return

        for entry_extra in self.renglones_extra:
            if entry_extra is not None and entry_extra.get().strip() == "":
                self.ventana_raiz.focus_set()
                return

    def _es_descendiente_de(self, widget, posible_padre):
        """
        Devuelve True si 'widget' está dentro de 'posible_padre' (es hijo/nieto/etc.).
        """
        if widget is None or posible_padre is None:
            return False

        actual = widget
        while actual is not None:
            if actual == posible_padre:
                return True
            actual = getattr(actual, "master", None)

        return False



    def _sin_accion_desplegar(self):
        """
        Acción placeholder para el botón desplegar.
        Por el momento no realiza ninguna acción.
        """
        return



    def _cargar_iconos_desplegar(self):
        """
        Carga los iconos del botón desplegar (normal y grande) según el modo actual,
        respetando el ángulo actual (self.angulo_desplegar).
        """
        self.imagen_desplegar_base = self._cargar_imagen_desplegar_base()

        self.icono_desplegar_normal = self._crear_icono_desplegar_ctk(
            angulo=self.angulo_desplegar,
            ancho=22,
            alto=22
        )

        self.icono_desplegar_grande = self._crear_icono_desplegar_ctk(
            angulo=self.angulo_desplegar,
            ancho=26,
            alto=26
        )



    def _al_entrar_boton_desplegar(self, evento=None):
        """
        Al pasar el cursor sobre el botón, agranda el icono.
        """
        if self.boton_desplegar is None or self.icono_desplegar_grande is None:
            return

        self.boton_desplegar.configure(image=self.icono_desplegar_grande)


    def _al_salir_boton_desplegar(self, evento=None):
        """
        Al quitar el cursor del botón, regresa el icono a su tamaño normal.
        """

        if self.boton_desplegar is None or self.icono_desplegar_normal is None:
            return

        self.boton_desplegar.configure(image=self.icono_desplegar_normal)



    def _cargar_imagen_desplegar_base(self):
        """
        Carga la imagen PIL base del icono desplegar según el modo actual.
        Intenta usar precarga para evitar leer del disco en el arranque.
        """
        try:
            import precarga
            if configuracion.MODO_OSCURO:
                base = precarga.obtener_recurso("imagen_desplegar_base_oscuro_rgba")
            else:
                base = precarga.obtener_recurso("imagen_desplegar_base_claro_rgba")

            if base is not None:
                # Copia para evitar efectos secundarios si alguien la reutiliza
                return base.copy()
        except Exception:
            pass

        if configuracion.MODO_OSCURO:
            ruta = obtener_ruta_icono_desplegar_oscuro()
        else:
            ruta = obtener_ruta_icono_desplegar_claro()

        return Image.open(ruta).convert("RGBA")




    def _crear_icono_desplegar_ctk(self, angulo: float, ancho: int, alto: int):
        """
        Crea un CTkImage rotado a un ángulo específico.
        """
        import customtkinter as ctk

        if self.imagen_desplegar_base is None:
            self.imagen_desplegar_base = self._cargar_imagen_desplegar_base()

        # PIL rota antihorario, por eso usamos -angulo para giro horario
        imagen_rotada = self.imagen_desplegar_base.rotate(-angulo, resample=Image.BICUBIC, expand=True)
        imagen_rotada = imagen_rotada.resize((ancho, alto), Image.LANCZOS)

        return ctk.CTkImage(light_image=imagen_rotada, dark_image=imagen_rotada, size=(ancho, alto))




    def _asegurar_renglones_extra(self):
        """
        Crea el contenedor y los renglones extra solo una vez.
        Se llama cuando el usuario despliega por primera vez.
        """
        if self.contenedor_renglones is not None:
            return

        if self.ventana_raiz is None:
            return

        # El contenedor se crea en la ventana raíz para poder colocarse por encima de las tarjetas.
        color_fondo_tarjeta = configuracion.COLOR_TARJETAS

        self.contenedor_renglones = ctk.CTkFrame(
            master=self.ventana_raiz,
            fg_color=color_fondo_tarjeta
        )
        self.contenedor_renglones.place_forget()

        # Creamos 4 renglones extra (junto con el principal suman 5)
        self._crear_renglones_extra()

        # Si el modo cambia antes de desplegar, al crear aquí ya toma el color actualizado.






    def _al_presionar_desplegar(self):
        """
        Alterna entre:
        - 1 renglón (solo self.cuadro_url)
        - 5 renglones (self.cuadro_url + 4 renglones extra)
        También rota el icono en seco: 0° <-> 180°
        """
        if self.boton_desplegar is None:
            return

        # Alternar estado
        self.desplegado = not self.desplegado


        # Si vamos a desplegar, aseguramos que los renglones extra existan
        if self.desplegado:
            self._asegurar_renglones_extra()


        # Rotación del icono (en seco)
        self.angulo_desplegar = 180 if self.desplegado else 0
        self._cargar_iconos_desplegar()
        self.boton_desplegar.configure(image=self.icono_desplegar_normal)


        # Mostrar u ocultar renglones extra
        if self.desplegado:
            self._mostrar_renglones_extra()
            self._mostrar_boton_x_principal()

            if self.cuadro_url is not None:
                self.cuadro_url.configure(placeholder_text=self.placeholder_url_lista)

            if self.etiqueta_url is not None:
                self.etiqueta_url.configure(text="Lista de URLs")

        else:
            self._ocultar_renglones_extra()
            self._ocultar_boton_x_principal()

            if self.cuadro_url is not None:
                self.cuadro_url.configure(placeholder_text=self.placeholder_url_normal)

            if self.etiqueta_url is not None:
                self.etiqueta_url.configure(text="URL")


        # Notificar que cambió el estado desplegado/oculto (afecta reglas del botón descargar)
        self._notificar_cambio_url()




    def _crear_renglones_extra(self):
        """
        Crea 4 CTkEntry adicionales (renglones 2 a 5).
        Se usan cuando el usuario despliega la lista.
        """
        if self.contenedor_renglones is None:
            return

        # Limpiar por si se vuelve a llamar
        for entry in self.renglones_extra:
            try:
                entry.destroy()
            except Exception:
                pass


        for boton in self.botones_x_extra:
            try:
                boton.destroy()
            except Exception:
                pass

        for contenedor in self.contenedores_renglones_extra:
            try:
                contenedor.destroy()
            except Exception:
                pass

        self.renglones_extra = []
        self.botones_x_extra = []
        self.contenedores_renglones_extra = []

        # Configuramos el contenedor para que los entries usen todo el ancho
        self.contenedor_renglones.grid_columnconfigure(0, weight=1)

        # Usar el mismo radio de esquina del entry principal para que se vean idénticos
        radio_esquinas = self.cuadro_url.cget("corner_radius") if self.cuadro_url is not None else None

        for i in range(3):
            # Contenedor por renglón (permite colocar la "x" encima del textbox)
            contenedor_renglon = ctk.CTkFrame(
                master=self.contenedor_renglones,
                fg_color="transparent"
            )
            contenedor_renglon.grid_columnconfigure(0, weight=1)

            configuracion_entry = {
                "master": contenedor_renglon,
                "placeholder_text": "•",
                "height": self.altura_entry if self.altura_entry is not None else 28
            }

            if radio_esquinas is not None:
                configuracion_entry["corner_radius"] = radio_esquinas

            if configuracion.COLOR_TEXBOX_URL_FONDO is not None:
                configuracion_entry["fg_color"] = configuracion.COLOR_TEXBOX_URL_FONDO

            if configuracion.COLOR_TEXBOX_URL_TEXTO is not None:
                configuracion_entry["text_color"] = configuracion.COLOR_TEXBOX_URL_TEXTO

            if configuracion.COLOR_TEXBOX_URL_PLACEHOLDER is not None:
                configuracion_entry["placeholder_text_color"] = configuracion.COLOR_TEXBOX_URL_PLACEHOLDER

            if configuracion.COLOR_TEXBOX_URL_BORDE is not None:
                configuracion_entry["border_color"] = configuracion.COLOR_TEXBOX_URL_BORDE

            entry_extra = ctk.CTkEntry(**configuracion_entry)
            entry_extra.grid(row=0, column=0, sticky="ew")


            # Detectar escritura/borrado en renglones extra
            entry_extra.bind("<KeyRelease>", self._al_cambiar_url)



            # Botón "x" del renglón extra:
            # Se pinta igual que el textbox para que no se vea el cuadro, solo la "x".
            color_fondo_x = configuracion.COLOR_TEXBOX_URL_FONDO
            if color_fondo_x is None:
                color_fondo_x = entry_extra.cget("fg_color")

            boton_x = ctk.CTkButton(
                master=contenedor_renglon,
                text="x",
                width=22,
                height=22,
                command=lambda e=entry_extra: self._borrar_entry(e),
                fg_color=color_fondo_x,
                bg_color="transparent",
                text_color=configuracion.COLOR_BOTON_X_TEXTO,
                hover=False,
                border_width=0,
                corner_radius=0
            )

            # Colocar encima del textbox, pegado a la derecha
            boton_x.place(relx=1.0, rely=0.5, anchor="e", x=-6)

            # Separación mínima e igual entre renglones
            pady_abajo = self.separacion_entre_renglones if i < 2 else 0
            contenedor_renglon.grid(row=i, column=0, sticky="ew", pady=(0, pady_abajo))

            self.contenedores_renglones_extra.append(contenedor_renglon)
            self.renglones_extra.append(entry_extra)
            self.botones_x_extra.append(boton_x)




    def _mostrar_renglones_extra(self):
        """
        Muestra los 4 renglones extra debajo del entry principal,
        sin mover el entry ni los botones.
        """
        if self.contenedor_renglones is None or self.cuadro_url is None:
            return

        # Asegurar que las medidas estén actualizadas
        self.tarjeta_padre.update_idletasks()

        # Coordenadas del entry principal respecto a la pantalla
        x_entry = self.cuadro_url.winfo_rootx()
        y_entry = self.cuadro_url.winfo_rooty()
        alto_entry = self.cuadro_url.winfo_height()
        ancho_entry = self.cuadro_url.winfo_width()

        # Coordenadas de la ventana raíz respecto a la pantalla
        x_ventana = self.ventana_raiz.winfo_rootx()
        y_ventana = self.ventana_raiz.winfo_rooty()

        # Convertir a coordenadas relativas a la ventana raíz
        x_rel = x_entry - x_ventana
        y_rel = (y_entry - y_ventana) + alto_entry + self.separacion_entre_renglones   # 6px de separación mínima


        # Calcular altura necesaria para 4 renglones extra + separación mínima
        separacion = self.separacion_entre_renglones
        altura_renglon = alto_entry
        altura_total = (3 * altura_renglon) + (2 * separacion)

        # Colocar el contenedor justo debajo del entry, mismo ancho
        # En CustomTkinter, width/height no se pasan en place(), se configuran en el widget
        self.contenedor_renglones.configure(width=ancho_entry, height=altura_total)

        # Evitar que el grid interno cambie el tamaño del contenedor
        self.contenedor_renglones.grid_propagate(False)

        # Forzar que cada renglón extra tenga el mismo tamaño del entry principal
        for entry_extra in self.renglones_extra:
            entry_extra.configure(width=ancho_entry, height=alto_entry)

        self.contenedor_renglones.place(
            x=x_rel,
            y=y_rel
        )

        # Asegurar que quede por encima de las demás tarjetas
        self.contenedor_renglones.lift()


    def _ocultar_renglones_extra(self):
        """
        Oculta los 4 renglones extra.
        """
        if self.contenedor_renglones is None:
            return
        self.contenedor_renglones.place_forget()