# precarga.py
# Módulo encargado de precargar recursos "pesados" (principalmente imágenes)
# mientras se muestra la pantalla de presentación (splash).
#
# Objetivo:
# - Reducir el "parpadeo" o la sensación de que la interfaz tarda en terminar de dibujarse
#   cuando aparece la ventana principal.
#
# Notas importantes:
# - Tkinter/CustomTkinter NO son seguros para manipularse desde hilos.
# - Aquí se usa el bucle de eventos (after) para ejecutar la precarga por tandas sin congelar la UI.

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

_cache_recursos: Dict[str, Any] = {}


def obtener_recurso(clave: str) -> Any:
    """Regresa un recurso precargado si existe; si no existe, regresa None."""
    return _cache_recursos.get(clave)


def guardar_recurso(clave: str, valor: Any) -> None:
    """Guarda (o reemplaza) un recurso en el cache."""
    _cache_recursos[clave] = valor


def limpiar_cache() -> None:
    """Limpia el cache completo de recursos."""
    _cache_recursos.clear()


def _tareas_precarga_estandar() -> List[Tuple[str, Callable[[], Any]]]:
    """Define tareas estándar de precarga (clave, función que crea el recurso)."""
    from PIL import Image
    import imagenes

    tareas: List[Tuple[str, Callable[[], Any]]] = []

    # Logos (Tkinter PhotoImage) usados en Presentacion
    tareas.append(("logo_luz_tk_320", lambda: imagenes.cargar_logo_modo_luz(ancho_maximo=320)))
    tareas.append(("logo_oscuro_tk_320", lambda: imagenes.cargar_logo_modo_oscuro(ancho_maximo=320)))

    # Iconos grandes (CTkImage) usados en la tarjeta derecha
    tareas.append(("icono_luz_ctk_170x230", lambda: imagenes.cargar_icono_luz_ctk(ancho=170, alto=230)))
    tareas.append(("icono_oscuro_ctk_170x230", lambda: imagenes.cargar_icono_oscuro_ctk(ancho=170, alto=230)))

    # Iconos del switch
    tareas.append(("icono_sol_ctk_14x14", lambda: imagenes.cargar_icono_sol_ctk(ancho=14, alto=14)))
    tareas.append(("icono_luna_ctk_14x14", lambda: imagenes.cargar_icono_luna_ctk(ancho=14, alto=14)))

    # Basura (normal y hover) para modo claro/oscuro
    tareas.append(("icono_basura_claro_ctk_22x22", lambda: imagenes.cargar_icono_basura_claro_ctk(ancho=22, alto=22)))
    tareas.append(("icono_basura_claro_ctk_26x26", lambda: imagenes.cargar_icono_basura_claro_ctk(ancho=26, alto=26)))
    tareas.append(("icono_basura_oscuro_ctk_22x22", lambda: imagenes.cargar_icono_basura_oscuro_ctk(ancho=22, alto=22)))
    tareas.append(("icono_basura_oscuro_ctk_26x26", lambda: imagenes.cargar_icono_basura_oscuro_ctk(ancho=26, alto=26)))

    # Descargar (normal y hover)
    tareas.append(("icono_descargar_ctk_22x22", lambda: imagenes.cargar_icono_descargar_ctk(tamanio=(22, 22))))
    tareas.append(("icono_descargar_ctk_26x26", lambda: imagenes.cargar_icono_descargar_ctk(tamanio=(26, 26))))

    # Desplegar: en URLTarjeta se rota el icono, aquí precargamos la base PIL RGBA
    tareas.append(("imagen_desplegar_base_claro_rgba", lambda: Image.open(imagenes.obtener_ruta_icono_desplegar_claro()).convert("RGBA")))
    tareas.append(("imagen_desplegar_base_oscuro_rgba", lambda: Image.open(imagenes.obtener_ruta_icono_desplegar_oscuro()).convert("RGBA")))

    return tareas


def precargar_recursos_en_tandas(
    ventana_tk: Any,
    al_terminar: Optional[Callable[[], None]] = None,
    *,
    milisegundos_entre_tandas: int = 1,
    tareas: Optional[List[Tuple[str, Callable[[], Any]]]] = None,
) -> None:
    """
    Precarga recursos sin bloquear la interfaz, ejecutando una tarea por iteración (tanda).

    Parámetros:
    - ventana_tk: instancia de tk.Tk (o widget) para usar after().
    - al_terminar: callback opcional cuando la precarga termina.
    - milisegundos_entre_tandas: pausa entre tareas; 1ms suele ser suficiente.
    - tareas: lista opcional de tareas (clave, creador). Si no se pasa, usa las estándar.
    """
    lista_tareas = tareas if tareas is not None else _tareas_precarga_estandar()
    pendientes: List[Tuple[str, Callable[[], Any]]] = list(lista_tareas)

    def _procesar_siguiente() -> None:
        if not pendientes:
            if al_terminar is not None:
                al_terminar()
            return

        clave, creador = pendientes.pop(0)

        if clave not in _cache_recursos:
            try:
                _cache_recursos[clave] = creador()
            except Exception:
                # Si un recurso falla, no detenemos el arranque.
                _cache_recursos[clave] = None

        ventana_tk.after(milisegundos_entre_tandas, _procesar_siguiente)

    ventana_tk.after(0, _procesar_siguiente)