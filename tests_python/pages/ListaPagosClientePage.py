from playwright.sync_api import Page, expect
from re import match

class ListaPagosClientePage:
    """
    Clase que representa la página donde se listan los pagos a facturas realizados por los clientes en la aplicación.
    Proporciona métodos para interactuar con los elementos de la página, validar el
    guardado """

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina
        self.__pagina.goto(
            f"{url}/compta/paiement/list.php?leftmenu=customers_bills_payment")
        
    def ingresar_ref_pago(self, ref_pago: str):
        """
        Ingresa el número de referencia de pago en el campo de búsqueda.

        Args:
            ref_pago (str): El número de referencia de pago a buscar.
        """
        assert ref_pago is not None, "El número de referencia de pago no puede ser nulo"

        self.__ref_pago = str(ref_pago)
        self.__pagina.locator("input[name='search_ref']").fill(str(ref_pago))

    def ingresar_fecha(self, fecha_inicio: str, fecha_fin: str):
        """
        Ingresa las fechas de inicio y fin en los campos de búsqueda.

        Args:
            fecha_inicio (str): La fecha de inicio en formato 'dd/mm/yyyy'.
            fecha_fin (str): La fecha de fin en formato 'dd/mm/yyyy'.
        """
        assert (fecha_inicio is not None) and (fecha_fin is not None), "La fecha de inicio no es válida"

        self.__pagina.locator("#search_date_start").fill(str(fecha_inicio))
        self.__pagina.locator("#search_date_end").fill(str(fecha_fin))
    
    def ingresar_tercero(self, tercero: str):
        """
        Ingresa el nombre del tercero en el campo de búsqueda.

        Args:
            tercero (str): El nombre del tercero a buscar.
        """
        assert tercero is not None, "El nombre del tercero no puede ser nulo"

        self.__tercero = str(tercero)
        self.__pagina.locator("input[name='search_company']").fill(str(tercero))

    def seleccionar_tipo_pago(self, tipo_pago: str):
        """
        Selecciona el tipo de pago en el campo de búsqueda.

        Args:
            tipo_pago (str): El tipo de pago a buscar.
        """
        assert tipo_pago is not None, "El tipo de pago no puede ser nulo"

        self.__tipo_pago = str(tipo_pago)
        self.__pagina.locator("#select2-selectsearch_paymenttype-container").click()
        if len(tipo_pago) == 0:
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option",name=str(tipo_pago)).click()

    def seleccionar_numero_cheque(self, numero: str):
        """
        Selecciona el número de cheque/transferencia en el campo de búsqueda.

        Args:
            numero (str): El número de cheque/transferencia a buscar.
        """
        assert numero is not None, "El número de cheque no puede ser nulo"

        self.__numero = str(numero)
        self.__pagina.locator("input[name='search_payment_num']").fill(str(numero))

    def seleccionar_cuenta_bancaria(self, cuenta: str):
        """
        Selecciona la cuenta bancaria en el campo de búsqueda.

        Args:
            cuenta (str): La cuenta bancaria a buscar.
        """
        assert cuenta is not None, "La cuenta bancaria no puede ser nula"

        self.__cuenta = str(cuenta)
        self.__pagina.locator("#select2-selectsearch_account-container").click()
        if len(cuenta) == 0:
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option",name=str(cuenta)).click()

    def ingresar_importe(self, importe: str):
        """
        Ingresa el importe en el campo de búsqueda.

        Args:
            importe (str): El importe a buscar.
        """
        assert importe is not None, "El importe no puede ser nulo"

        self.__importe = str(importe)
        self.__pagina.locator("input[name='search_amount']").fill(str(importe))
    
    def aplicar_filtros(self):
        """
        Aplica los filtros de búsqueda.
        """
        self.__pagina.locator("button[name='button_search_x']").click()

    def verificar_tabla_vacia(self):
        """
        Verifica si la tabla de pagos está vacía.
        """
        expect(self.__pagina.locator("xpath=//td//span[@class='opacitymedium']")).to_be_visible()
    
    def verificar_error(self, mensaje: str):
        """
        Verifica si se muestra un mensaje de error en la página.

        Args:
            mensaje (str): El mensaje de error esperado.
        """
        COMPONENTE = self.__pagina.locator("div[class='jnotify-message']")
        expect(COMPONENTE).to_be_visible()
        expect(COMPONENTE).to_contain_text(str(mensaje))
    
    def __convertir_numero(self, numero: str):
        """
        Convierte un número en formato string a float.

        Args:
            numero (str): El número a convertir.

        Returns:
            float: El número convertido.
        """
        numero = numero.replace(".","")
        numero = numero.replace(",",".")
        return float(numero)

    def __verificar_celdas(self, cuentas: list, ref: str):
        """
        Verifica si las cuentas bancarias son correctas.

        Args:
            cuentas (list): Lista de cuentas bancarias esperadas.
            ref (str): Valor esperado.
        """
        for cuenta in cuentas:
            expect(cuenta).to_contain_text(str(ref))

    def __verificar_importes(self, importes: list):
        """"
        Verifica si los importes son correctos.
        
        Args:
            importes (list[str]): Importes de la tabla.
        """
        OPERADORES = (">=","<=","<",">","!=")
        operador = "="
        valor = 0
        for i in OPERADORES:
            if len(self.__importe.split(i))>1:
                operador = i
                valor = self.__convertir_numero(self.__importe.split(i)[1])
                break
        for i in importes:
            i = self.__convertir_numero(i.inner_text())
            match(operador):
                case "=":
                    assert i == valor, f"El importe {i} no es igual a {valor}."
                case ">=":
                    assert i >= valor, f"El importe {i} no es mayor o igual a {valor}."
                case "<=":
                    assert i <= valor, f"El importe {i} no es menor o igual a {valor}."
                case ">":
                    assert i > valor, f"El importe {i} no es mayor a {valor}."
                case "<":
                    assert i < valor, f"El importe {i} no es menor a {valor}."
                case "!=":
                    assert i != valor, f"El importe {i} no es diferente a {valor}."

    def verificar_filtro(self, total: str):
        """
        Verifica si el total de la tabla de pagos es correcto.

        Args:
            total (str): El total esperado.
        """

        # Verificando que se haya aplicado el filtro de cuenta bancaria
        if self.__cuenta != "":
            CUENTAS = self.__pagina.locator("span[class='fas fa-university infobox-bank_account paddingright']").all()
            self.__verificar_celdas(CUENTAS, self.__cuenta)

        if self.__tercero != "":
            TERCEROS = self.__pagina.locator("a[class='classfortooltip refurl valignmiddle']").all()
            self.__verificar_celdas(TERCEROS, self.__tercero)

        if self.__tipo_pago != "":
            TIPOS = self.__pagina.get_by_role("cell",name=self.__tipo_pago).all()
            self.__verificar_celdas(TIPOS, self.__tipo_pago)

        if self.__ref_pago != "":
            REFS = self.__pagina.get_by_role("link",name=self.__ref_pago).all()
            self.__verificar_celdas(REFS, self.__ref_pago)

        if self.__numero != "":
            NUMEROS = self.__pagina.get_by_role("cell",name=self.__numero).all()[1:]
            self.__verificar_celdas(NUMEROS, self.__numero)

        if self.__importe != "":
            IMPORTES = self.__pagina.locator("span[class='amount']").all()
            self.__verificar_importes(IMPORTES)

        # verificando el total
        expect(self.__pagina.locator("xpath=//tr[@class='liste_total']//td[@class='right']")).to_contain_text(str(total))

    def verificar_tipo_inexistente(self, tipo: str):
        """
        Verifica si el tipo de pago es inexistente.

        Args:
            tipo (str): El tipo de pago a probar.
        """
        self.__pagina.locator("#select2-selectsearch_paymenttype-container").click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(tipo))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_contain_text("No se han encontrado resultados")

    def verificar_cuenta_inexistente(self, cuenta: str):
        """
        Verifica si la cuenta bancaria es inexistente.

        Args:
            cuenta (str): La cuenta bancaria a probar.
        """
        self.__pagina.locator("#select2-selectsearch_account-container").click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(cuenta))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_contain_text("No se han encontrado resultados")