import customtkinter as ctk
import configuracion
from imagenes import cargar_icono_descargar_ctk
from funcionamiento.descargar import actualizar_visibilidad_boton_descargar


class ProgresoTarjeta:
    """
    Componente de barra de progreso para colocarse dentro de una tarjeta.
    - Se centra automáticamente.
    - Usa relwidth para que no se salga de la tarjeta.
    """

    def __init__(self, tarjeta_padre):
        self.tarjeta_padre = tarjeta_padre
        self.barra_progreso = None
        self.boton_descargar = None
        self.icono_descargar = None
        self.icono_descargar_normal = None
        self.icono_descargar_grande = None
        self.tarjeta_url = None
        self.tarjeta_formato = None
        self.tarjeta_aviso = None

    def crear(self):
        """
        Crea la barra de progreso centrada dentro de la tarjeta.
        """

        self.barra_progreso = ctk.CTkProgressBar(
            master=self.tarjeta_padre,
            height=30
        )

        # Aplicar tema antes de mostrarla para evitar que se vea el color por defecto
        self.aplicar_tema()

        # Valor inicial (0%)
        self.barra_progreso.set(0.0)

        # Centrada y con ancho relativo para que no se salga de la tarjeta
        self.barra_progreso.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.80)




        # Iconos del botón descargar (normal y grande) para efecto hover
        self.icono_descargar_normal = cargar_icono_descargar_ctk(tamanio=(22, 22))
        self.icono_descargar_grande = cargar_icono_descargar_ctk(tamanio=(26, 26))

        self.boton_descargar = ctk.CTkButton(
            master=self.tarjeta_padre,
            text="",
            image=self.icono_descargar_normal,
            width=32,
            height=32,
            corner_radius=10,
            fg_color="transparent",
            hover=False,
            command=self._al_presionar_descargar
        )


        # Reposicionar si cambia el tamaño de la tarjeta (para mantener el margen derecho)
        self.tarjeta_padre.bind("<Configure>", self._reposicionar_boton_descargar, add="+")
        # Esquina superior derecha con margen (x negativo separa del borde derecho)

        # Eventos hover para agrandar/reducir el icono del botón descargar
        self.boton_descargar.bind("<Enter>", self._al_entrar_boton_descargar)
        self.boton_descargar.bind("<Leave>", self._al_salir_boton_descargar)

        margen = 12

        # Colocar con el mismo margen arriba y derecha de forma exacta
        self.tarjeta_padre.update_idletasks()
        ancho_boton = self.boton_descargar.winfo_reqwidth()

        self.boton_descargar.place(
            x=self.tarjeta_padre.winfo_width() - ancho_boton - margen,
            y=margen
        )

        # Aplicar tema inicial
        self.aplicar_tema()

    def aplicar_tema(self):
        """
        Aplica colores del tema actual.
        Nota: No forzamos un color de progreso específico para no romper tu estilo;
        solo ajustamos el fondo para que combine con la tarjeta.
        """
        if self.barra_progreso is None:
            return

        # Fondo de la barra igual al color de la tarjeta para que se vea integrada
        # fg_color = riel (fondo) de la barra
        # progress_color = color del relleno (avance)
        self.barra_progreso.configure(
            fg_color=configuracion.COLOR_BARRA_PROGRESO_FONDO,
            progress_color=configuracion.COLOR_BARRA_PROGRESO_RELLENO
        )


        # Recargar iconos del botón descargar para el modo actual (normal y hover)
        self.icono_descargar_normal = cargar_icono_descargar_ctk(tamanio=(22, 22))
        self.icono_descargar_grande = cargar_icono_descargar_ctk(tamanio=(26, 26))

        if self.boton_descargar is not None:
            self.boton_descargar.configure(image=self.icono_descargar_normal)


    def establecer_progreso(self, valor):
        """
        Establece el progreso.
        'valor' debe estar entre 0.0 y 1.0.

        Importante:
        - La descarga irá en un hilo aparte.
        - Tkinter/CustomTkinter NO permite actualizar widgets desde otro hilo.
        - Por eso usamos after() para actualizar en el hilo principal.
        """
        if self.barra_progreso is None:
            return

        # Asegurar rango válido
        if valor < 0:
            valor = 0
        elif valor > 1:
            valor = 1

        def _aplicar():
            if self.barra_progreso is not None:
                self.barra_progreso.set(valor)

        # Programar actualización en el hilo principal
        try:
            self.tarjeta_padre.after(0, _aplicar)
        except Exception:
            # Fallback (por si algo raro pasa)
            _aplicar()


    def _al_presionar_descargar(self):
        """
        Acción del botón de descargar.
        Ejecuta la descarga en un hilo para no congelar la interfaz.
        """
        import threading
        from funcionamiento.analizar import al_presionar_descargar

        # Evitar doble click mientras descarga
        if self.boton_descargar is not None:
            self.boton_descargar.configure(state="disabled")

        # Reiniciar barra al iniciar
        self.establecer_progreso(0.0)


        def tarea():
            resultado_descarga = False
            try:
                resultado_descarga = al_presionar_descargar(
                    tarjeta_url=self.tarjeta_url,
                    tarjeta_formato=self.tarjeta_formato,
                    establecer_progreso=self.establecer_progreso,
                    contenedor_tooltip=self.tarjeta_aviso
                )
            except Exception as e:
                print(f"[progreso] Error en descarga: {e}")
                resultado_descarga = False
            finally:
                def _finalizar():
                    if self.boton_descargar is not None:
                        self.boton_descargar.configure(state="normal")

                    if not resultado_descarga:
                        self.establecer_progreso(0.0)
                        return

                    self.establecer_progreso(1.0)
                    self.tarjeta_padre.after(800, lambda: self.establecer_progreso(0.0))

                try:
                    self.tarjeta_padre.after(0, _finalizar)
                except Exception:
                    _finalizar()




        hilo = threading.Thread(target=tarea, daemon=True)
        hilo.start()



    def _reposicionar_boton_descargar(self, evento):
        """
        Mantiene el mismo margen arriba y derecha para el botón, incluso si la tarjeta cambia de tamaño.
        """
        if self.boton_descargar is None:
            return

        # Si el botón está oculto (place_forget), no lo volvemos a mostrar
        try:
            if not self.boton_descargar.winfo_ismapped():
                return
        except Exception:
            pass

        margen = 12
        ancho_boton = self.boton_descargar.winfo_reqwidth()

        self.boton_descargar.place(
            x=evento.width - ancho_boton - margen,
            y=margen
        )


    def _al_entrar_boton_descargar(self, evento=None):
        """
        Al pasar el cursor sobre el botón, agranda el icono.
        """
        if self.boton_descargar is None or self.icono_descargar_grande is None:
            return
        self.boton_descargar.configure(image=self.icono_descargar_grande)


    def _al_salir_boton_descargar(self, evento=None):
        """
        Al quitar el cursor del botón, regresa el icono a su tamaño normal.
        """
        if self.boton_descargar is None or self.icono_descargar_normal is None:
            return
        self.boton_descargar.configure(image=self.icono_descargar_normal)



    def establecer_visibilidad_boton_descargar(self, visible: bool):
        """
        Delegamos la visibilidad/posicionamiento del botón a funcionamiento/descargar.py
        """
        actualizar_visibilidad_boton_descargar(
            boton_descargar=self.boton_descargar,
            tarjeta_padre=self.tarjeta_padre,
            visible=visible
        )




    def conectar_tarjetas(self, tarjeta_url, tarjeta_formato, tarjeta_aviso=None):
        self.tarjeta_url = tarjeta_url
        self.tarjeta_formato = tarjeta_formato
        self.tarjeta_aviso = tarjeta_aviso
