# funcionamiento/analizar.py

def al_presionar_descargar(tarjeta_url, tarjeta_formato, establecer_progreso=None):
    """
    Se llama cuando se presiona el botón de descargar.

    - Si NO está desplegada la lista:
        descarga solo el renglón principal.

    - Si SÍ está desplegada:
        toma todos los renglones que tengan contenido (principal + extras),
        crea una lista lógica y descarga cada URL.
        La barra se divide en partes iguales según el número de URLs.
    """

    if tarjeta_url is None or tarjeta_formato is None:
        print("[analizar] No hay referencias a tarjeta_url/tarjeta_formato.")
        return

    # Obtener formato y ruta (se usan en ambos casos)
    formato = tarjeta_formato.select_formato.get().strip()
    ruta_guardado = tarjeta_formato.cuadro_ruta.get().strip()

    formato_normalizado = formato.replace("•", "").strip().lower()

    def _descargar_una_url(url, progreso_callback=None):
        """
        Enruta a la función correspondiente según el formato seleccionado.
        """
        if formato_normalizado == "mp4":
            from funcionamiento.formatos.mp4 import descargar_mp4
            descargar_mp4(url, ruta_guardado, progreso_callback)
            return

        if formato_normalizado == "mp3":
            from funcionamiento.formatos.mp3 import descargar_mp3
            descargar_mp3(url, ruta_guardado, progreso_callback)
            return

        if formato_normalizado == "short":
            from funcionamiento.formatos.short import descargar_short
            descargar_short(url, ruta_guardado, progreso_callback)
            return

        print("[analizar] Formato no válido o no seleccionado. No se hace nada.")

    # -------------------------
    # CASO 1: Lista desplegada
    # -------------------------
    if tarjeta_url.desplegado:
        # Tomar principal + extras, quedarse con los que sí tienen texto
        urls = []

        # Principal
        if tarjeta_url.cuadro_url is not None:
            texto = tarjeta_url.cuadro_url.get().strip()
            if texto:
                urls.append(texto)

        # Extras (en tu URL.py: self.renglones_extra es una lista de CTkEntry)
        for entry_extra in getattr(tarjeta_url, "renglones_extra", []):
            if entry_extra is None:
                continue
            texto = entry_extra.get().strip()
            if texto:
                urls.append(texto)

        cantidad = len(urls)

        print(f"[analizar] Lista desplegada. URLs con contenido = {cantidad}")
        print(f"[analizar] formato = {formato}")
        print(f"[analizar] ruta_guardado = {ruta_guardado}")

        if cantidad == 0:
            print("[analizar] No hay URLs con contenido. No se descarga nada.")
            return

        # Descargar secuencialmente y dividir progreso en segmentos
        for i, url in enumerate(urls):

            def progreso_segmentado(valor, indice=i, total=cantidad):
                """
                Convierte el progreso 0..1 de UNA descarga
                a progreso global dividido por segmentos.
                """
                if not callable(establecer_progreso):
                    return

                # Asegurar rango
                if valor < 0:
                    valor = 0
                elif valor > 1:
                    valor = 1

                progreso_global = (indice + valor) / total
                establecer_progreso(progreso_global)

            print(f"[analizar] Descargando ({i+1}/{cantidad}) -> {url}")

            # Descargar una URL (progreso mapeado)
            _descargar_una_url(url, progreso_segmentado)

            # Al terminar esa URL, fijar el final de su segmento
            if callable(establecer_progreso):
                establecer_progreso((i + 1) / cantidad)

        return

    # -------------------------
    # CASO 2: NO desplegada
    # -------------------------
    URL = tarjeta_url.cuadro_url.get().strip() if tarjeta_url.cuadro_url is not None else ""

    print(f"[analizar] URL = {URL}")
    print(f"[analizar] formato = {formato}")
    print(f"[analizar] ruta_guardado = {ruta_guardado}")

    _descargar_una_url(URL, establecer_progreso)