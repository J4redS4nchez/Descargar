# ventana.py
# Módulo encargado de la interfaz principal (ventana y controles).
# Por ahora NO descarga nada; solo construye la UI.

import tkinter as tk
from tkinter import ttk
from imagenes import cargar_logo_modo_luz
from presentacion import Presentacion
from componentes.switch_MODO import SwitchModo
from componentes.tarjetas import TarjetasLayout
import configuracion
import precarga




class VentanaPrincipal:
    def __init__(self):
        # Ventana base
        self.ventana = tk.Tk()
        self.ventana.withdraw()  # Oculta mientras se prepara (evita ventana chiquita)

        self.ventana.title("Eemsik")
        self.ventana.resizable(False, False)
        # Aplica el color de fondo según la configuración (claro/oscuro)
        self.ventana.configure(bg=configuracion.COLOR_FONDO_VENTANA)


        ancho_ventana = 900
        alto_ventana = 500
        self._centrar_ventana(ancho_ventana, alto_ventana)

        # Variables de la interfaz
        self.url = tk.StringVar(value="")
        self.formato = tk.StringVar(value="mp4")
        self.porcentaje = tk.DoubleVar(value=0.0)

        # Componente switch (se crea en _crear_componentes)
        self.switch_modo = None


        # Referencia a la imagen para evitar que el recolector de basura la elimine
        self.logo_tk = None

        #Referencia a las tarjetas para ayudar a la interfaz
        self.tarjetas = None

        # Mostrar presentación (splash)
        self.presentacion = Presentacion(self.ventana)
        self.presentacion.mostrar()

        self.ventana.deiconify()  # Muestra ya lista con el splash

        # Banderas para coordinar: precarga + tiempo del splash
        self._precarga_lista = False
        self._tiempo_splash_cumplido = False
        self._interfaz_iniciada = False

        # Inicia precarga mientras se muestra la presentación (sin congelar)
        precarga.precargar_recursos_en_tandas(
            self.ventana,
            al_terminar=self._al_terminar_precarga,
            milisegundos_entre_tandas=1
        )

        # Respeta tu duración de splash (3000 ms)
        self.ventana.after(3000, self._al_terminar_splash)




    def _crear_componentes(self):
        """Crea únicamente las tarjetas (layout base)."""
        # Aplica el color de fondo según la configuración actual (claro/oscuro)
        self.ventana.configure(bg=configuracion.COLOR_FONDO_VENTANA)


        self.tarjetas = TarjetasLayout(self.ventana, color_tarjeta=configuracion.COLOR_TARJETAS)
        self.tarjetas.crear()


    def _al_pulsar_descargar(self):
        """Acción temporal del botón Descargar."""
        self.porcentaje.set(0.0)
        self.etiqueta_porcentaje.config(text="0%")

    def ejecutar(self):
        """Inicia la aplicación."""
        self.ventana.mainloop()

    def _centrar_ventana(self, ancho: int, alto: int):
        """Centra la ventana en la pantalla usando el tamaño indicado."""
        self.ventana.update_idletasks()  # asegura que Tk tenga datos de pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _iniciar_interfaz(self):
        """Oculta la presentación y construye la interfaz principal."""
        # Ocultamos para que no se vea el proceso de construcción y pintado de widgets
        self.ventana.withdraw()

        # Quitamos el splash
        self.presentacion.ocultar()

        # Construimos la UI
        self._crear_componentes()

        # Forzamos a que Tk calcule geometría y pinte todo antes de mostrar
        self.ventana.update_idletasks()

        # Mostramos ya lista
        self.ventana.deiconify()


    def _al_cambiar_modo(self, esta_oscuro):
        """Callback del switch. Por ahora no aplica tema; queda listo para después."""
        pass




    def _al_terminar_precarga(self):
        """Marca que la precarga terminó y verifica si ya se puede iniciar la UI."""
        self._precarga_lista = True
        self._intentar_iniciar_interfaz()

    def _al_terminar_splash(self):
        """Marca que ya pasó el tiempo del splash y verifica si ya se puede iniciar la UI."""
        self._tiempo_splash_cumplido = True
        self._intentar_iniciar_interfaz()

    def _intentar_iniciar_interfaz(self):
        """
        Inicia la interfaz principal solo cuando:
        - ya terminó la precarga, y
        - ya pasó el tiempo del splash,
        evitando doble ejecución.
        """
        if self._interfaz_iniciada:
            return

        if not self._precarga_lista:
            return

        if not self._tiempo_splash_cumplido:
            return

        self._interfaz_iniciada = True
        self._iniciar_interfaz()