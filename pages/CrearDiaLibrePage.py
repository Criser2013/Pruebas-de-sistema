from playwright.sync_api import Page, expect, Dialog

class  CrearDiaLibrePage:
    """
    Clase que representa la página para crear un día libre en la aplicación.
    Proporciona métodos para interactuar con los elementos de la página, validar el
    guardado de datos y demás pruebas.
    """
    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina
        self.__descripcion = ""
        self.__usuario = ""
        self.__tipo_dia_libre = ""
        self.__fecha_inicio = ""
        self.__fecha_fin = ""
        self.__jornada_inicio = ""
        self.__jornada_fin = ""
        self.__revisor = ""
        self.__msg_dialogo = ""
        self.__pagina.on("dialog", self.__obtener_texto_dialogo)
        self.__pagina.goto(
            f"{url}/holiday/card.php?mainmenu=hrm&leftmenu=holiday&action=create")

    def seleccionar_usuario(self, usuario: str):
        """
        Selecciona el usuario que solicita los días libres.

        Args:
            usuario (str): Nombre del usuario a seleccionar.
        """

        if ((usuario is not None) and (len(usuario) > 0)):
            self.__usuario = str(usuario)
            self.__pagina.locator("span#select2-fuserid-container").click()
            self.__pagina.get_by_role("option", name=str(usuario)).click()
        else:
            raise Exception("El nombre de usuario no puede estar vacío.")

    def seleccionar_tipo_dia_libre(self, tipo: str = "&nbsp"):
        """
        Selecciona el tipo de día libre que se solicita.

        Args:
            tipo (str): Nombre del tipo de día libre. De forma predeterminada se selecciona la opción vacía.
        """
        if tipo is not None:
            self.__tipo_dia_libre = str(tipo)
            self.__pagina.locator("#select2-type-container").click()
            self.__pagina.get_by_role("option", name=str(tipo)).click()
        else:
            raise Exception("El tipo de día libre ingresado no es válido.")

    def seleccionar_fecha_inicio(self, fecha: str, jornada: str):
        """
        Selecciona la fecha de inicio y la jornada del día libre.

        Args:
            fecha (str): Fecha en que inicia el día libre. Debe estar en formato DD/MM/AAAA.
            jornada (str): Jornada a seleccionar (Mañana, Tarde).
        """

        if jornada in ("Mañana", "Tarde"):
            self.__fecha_inicio = str(fecha)
            self.__jornada_inicio = str(jornada)
            self.__pagina.locator("#date_debut_").fill(str(fecha))
            self.__pagina.locator("#select2-starthalfday-container").click()
            self.__pagina.get_by_role("option", name=str(jornada)).click()
        else:
            raise Exception("La jornada no es válida. Debe ser 'Mañana' o 'Tarde'.")

    def seleccionar_fecha_fin(self, fecha: str, jornada: str):
        """
        Selecciona la fecha de finalización y la jornada del día período de días librea.

        Args:
            fecha (str): Fecha en que termina el período de días libres. Debe estar en formato DD/MM/AAAA.
            jornada (str): Jornada a seleccionar (Mañana, Tarde).
        """

        if jornada in ("Mañana", "Tarde"):
            self.__fecha_fin = str(fecha)
            self.__jornada_fin = str(jornada)
            self.__pagina.locator("#date_fin_").fill(str(fecha))
            self.__pagina.locator("#select2-endhalfday-container").click()
            self.__pagina.get_by_role("option", name=str(jornada)).click()
        else:
            raise Exception("La jornada no es válida. Debe ser 'Mañana' o 'Tarde'.")

    def seleccionar_revisor(self, revisor: str = "&nbsp"):
        """
        Selecciona el usuario que revisará la solicitud de días libres.

        Args:
            revisor (str): Nombre del revisor que revisaá la solicitud.
            De forma predeterminada se selecciona la opción vacía.
        """
        if revisor is not None:
            self.__revisor = str(revisor)
            self.__pagina.locator("span[id='select2-valideur-container']").click()
            self.__pagina.get_by_role("option", name=str(revisor)).click()
        else:
            raise Exception("El revisor ingresado no es válido.")

    def ingresar_descripcion(self, descripcion: str):
        """
        Ingresa la descripción de la solicitud de días libres.

        Args:
            descripcion (str): Descripción de la solicitud de días libres. Puede ser texto HTML.
        """

        if ((descripcion is not None) and (len(descripcion) > 0)):
            self.__descripcion = str(descripcion)
            # Clic al botón para la descripción en HTML
            self.__pagina.locator("#cke_46").click()

            # Colocando texto en la descripción (HTML)
            self.__pagina.locator(
                "xpath=//textarea[@class='cke_source cke_reset cke_enable_context_menu cke_editable cke_editable_themed cke_contents_ltr']"
            ).fill(str(descripcion))
        else:
            raise Exception("La descripción no puede estar vacía.")
    
    def guardar_datos(self):
        """
        Guarda la solicitud de días libres. Este método hace clic sobre el botón de guardar
        """

        self.__pagina.get_by_role("button", name="Crear solicitud de licencia").click()

    def verificar_guardado(self, nombre_archivo: str):
        """
        Verifica que los datos se hayan guardado correctamente y toma una captura de pantalla.

        Args:
            nombre_archivo (str): Nombre del archivo para la captura de pantalla. No debe contener la extensión ni la ruta.
        """

        TOKENS = str(nombre_archivo).split(".") if nombre_archivo is not None else "*.*"

        if len(TOKENS) == 1:
            expect(self.__pagina.get_by_text(self.__usuario)).to_be_visible()
            expect(self.__pagina.get_by_text(self.__tipo_dia_libre)).to_be_visible()
            expect(self.__pagina.get_by_text(self.__fecha_inicio)).to_be_visible()
            expect(self.__pagina.get_by_text(self.__fecha_fin)).to_be_visible()
            expect(self.__pagina.get_by_text(self.__revisor)).to_be_visible()
            expect(self.__pagina.get_by_text(self.__descripcion)).to_be_visible()

            # Verificando la marca de tiempo de grabación
            TIEMPO = self.__pagina.locator("span[class=opacitymedium]").all()

            expect(TIEMPO[0]).to_contain_text(self.__jornada_inicio)
            expect(TIEMPO[1]).to_contain_text(self.__jornada_fin)
            self.__pagina.screenshot(path=f"screenshots/{str(nombre_archivo)}.png")
        else:
            raise Exception("El nombre de archivo ingresado no es válido. Recuerde que no debe ingresar una extensión")
    
    def verificar_error_fechas_no_selec(self, inicio: bool):
        """
        Verifica que la fecha de inicio sea válida.

        Args:
            inicio (bool): Indica si se está verificando la fecha de inicio o de finalización.
        """
        texto = "inicio"
        self.guardar_datos()
        if not inicio:
            texto = "finalización"

        self.__verificar_dialogo(f"Debes seleccionar una fecha de {texto}.")
    
    def verificar_error_no_revisor(self):
        """
        Verifica que se muestre un mensaje de error en el navegador cuando no se selecciona un revisor.
        """
        self.guardar_datos()
        self.__verificar_dialogo("Debe elegir al aprobador para su solicitud de licencia.")
    
    def verificar_error_modal(self, texto: str):
        """
        Verifica que se muestre un modal de error en el navegador que contenga elñ texto dado.

        Args:
            texto (str): Texto que se espera que contenga el modal de error.
        """
        self.guardar_datos()
        expect(self.__pagina.locator(".jnotify-message")).to_contain_text(str(texto))
    
    def verificar_revisor_no_existente(self, revisor: str):
        if revisor is not None:
            self.__revisor = str(revisor)
            self.__pagina.locator("span[id='select2-valideur-container']").click()
            ELEMENTOS = self.__pagina.locator(".select2-results__option").all()

            for i in ELEMENTOS:
                expect(i).not_to_have_text(str(revisor))
        else:
            raise Exception("El revisor ingresado no es válido.")
        
    def __obtener_texto_dialogo(self, dialogo: Dialog):
        """
        Cierra el diálogo y obtiene el texto del mensaje.

        Args:
            dialogo (Dialog): Objeto de diálogo que contiene el mensaje.
        """
        dialogo.accept()
        self.__msg_dialogo = dialogo.message
    
    def __verificar_dialogo(self, texto: str):
        """
        Verifica que el diálogo contenga el texto esperado.

        Args:
            texto (str): Texto esperado en el diálogo.
        """
        if self.__msg_dialogo != texto:
            raise Exception(f"El mensaje del diálogo no es el esperado. Se esperaba: {texto} y se obtuvo: {self.__msg_dialogo}")