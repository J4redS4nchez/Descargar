# funcionamiento/analizar.py

def al_presionar_descargar(tarjeta_url, tarjeta_formato, establecer_progreso=None):
    """
    Se llama cuando se presiona el botón de descargar.

    - Si NO está desplegada la lista de URLs:
        - Obtiene el texto del textbox principal (URL) y lo guarda en la variable URL.
        - Obtiene el formato del selectbox.
        - Obtiene la ruta del textbox de ruta.
        - Enruta a la función correspondiente (mp4/mp3/short).
    """

    # Validaciones mínimas para no romper si aún no conectaste referencias
    if tarjeta_url is None or tarjeta_formato is None:
        print("[analizar] No hay referencias a tarjeta_url/tarjeta_formato.")
        return

    # 1) Revisar si la lista está desplegada
    # (en tu URLTarjeta existe: self.desplegado)
    if tarjeta_url.desplegado:
        # Por ahora: si está desplegado, todavía NO hacemos nada (lo hacemos después)
        print("[analizar] La lista está desplegada. Aún no implementado en este paso.")
        return

    # 2) Obtener URL del textbox principal (cuando NO está desplegado)
    URL = tarjeta_url.cuadro_url.get().strip()

    # 3) Obtener formato del selectbox
    # En tu FormatoTarjeta existe: self.select_formato (CTkComboBox)
    formato = tarjeta_formato.select_formato.get().strip()

    # 4) Obtener ruta del textbox de ruta
    # En tu FormatoTarjeta existe: self.cuadro_ruta (CTkEntry)
    ruta_guardado = tarjeta_formato.cuadro_ruta.get().strip()

    print(f"[analizar] URL = {URL}")
    print(f"[analizar] formato = {formato}")
    print(f"[analizar] ruta_guardado = {ruta_guardado}")

    # Si quieres, aquí más adelante pondremos validaciones (URL vacía, ruta vacía, etc.)
    # pero en este paso solo lo dejamos listo para enrutar.

    # Normalizar formato: tu combo trae cosas como " mp4", " mp3", " short"
    formato_normalizado = formato.replace("•", "").strip().lower()

    # 5) Enrutar al archivo correspondiente
    if formato_normalizado == "mp4":
        from funcionamiento.formatos.mp4 import descargar_mp4
        descargar_mp4(URL, ruta_guardado, establecer_progreso)
        return

    if formato_normalizado == "mp3":
        from funcionamiento.formatos.mp3 import descargar_mp3
        descargar_mp3(URL, ruta_guardado, establecer_progreso)
        return

    if formato_normalizado == "short":
        from funcionamiento.formatos.short import descargar_short
        descargar_short(URL, ruta_guardado, establecer_progreso)
        return

    # Si cae aquí, no seleccionó nada válido (o dejó los puntitos)
    print("[analizar] Formato no válido o no seleccionado. No se hace nada.")