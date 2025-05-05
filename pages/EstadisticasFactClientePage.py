from playwright.sync_api import Page, expect
from re import match

class  EstadisticasFactClientePage:
    """
    Clase que representa la página de estadísticas de las facturas creadas a clientes en la aplicación.
    Proporciona métodos para interactuar con los elementos de la página, validar el
    guardado """

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina
        self.__pagina.goto(
            f"{url}/compta/facture/stats/index.php")
    
    def seleccionar_tercero(self, tercero: str):
        """
        Selecciona un tercero en la página de estadísticas de las facturas creadas a clientes.

        Args:
            tercero (str): Nombre del tercero a seleccionar.
        """
        assert tercero is not None, "El tercero no puede estar vacío."
        COMPONENTE = self.__pagina.locator("span[class='select2-selection select2-selection--single flat widthcentpercentminusx maxwidth300']").all()[0]
        COMPONENTE.click()

        if len(tercero) == 0:
            self.__pagina.wait_for_timeout(1000)
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(tercero)).click()
    
    def seleccionar_tipo_tercero(self, tipo_tercero: str):
        """
        Selecciona el tipo de tercero en la página de estadísticas de las facturas creadas a clientes.

        Args:
            tipo_tercero (str): Tipo de tercero a seleccionar.
        """
        assert tipo_tercero is not None, "El tipo de tercero no puede estar vacío."

        self.__pagina.locator("#select2-typent_id-container").click()

        if len(tipo_tercero) == 0:
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(tipo_tercero)).click()

    def seleccionar_etiqueta(self,etiqueta: str|tuple):
        """
        Selecciona una o varias etiquetas en la página de estadísticas de las facturas creadas a clientes.

        Args:
            etiqueta (str|tuple): Etiqueta o tupla de etiquetas a seleccionar.
        """
        assert (etiqueta is not None) and (len(etiqueta) > 0), "La etiqueta no puede estar vacía."
        if isinstance(etiqueta, tuple):
            for i in etiqueta:
                self.__pagina.locator("ul[class=select2-selection__rendered]").click()
                self.__pagina.get_by_role("option", name=str(i)).click()
        else:
            self.__pagina.locator("ul[class=select2-selection__rendered]").click()
            self.__pagina.get_by_role("option", name=str(etiqueta)).click()
    
    def seleccionar_creador(self, creador: str):
        """
        Selecciona el filtro "creado por".

        Args:
            creador (str): Nombre del creador de la factura a seleccionar.
        """
        assert creador is not None, "El creador no puede estar vacío."
        self.__pagina.locator("#select2-userid-container").click()

        if len(creador) == 0:
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(creador)).click()
    
    def seleccionar_estado(self, estado: str):
        """
        Selecciona el filtro "estado".

        Args:
            estado (str): Estado de la factura a seleccionar.
        """
        assert estado is not None, "El estado no puede estar vacío."
        self.__pagina.locator("#select2-object_status-container").click()

        if len(estado) == 0:
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(estado)).click()
    
    def seleccionar_ano(self, ano: str):
        """
        Selecciona el filtro "año".

        Args:
            ano (str): Año de la factura a seleccionar.
        """
        assert (ano is not None) and (len(ano) > 0), "El año no puede estar vacío."
        assert match(r"^[1-2]\d{3}$", ano) is not None, "El año debe ser un número de 4 dígitos."

        self.__ano = str(ano)
        self.__pagina.locator("#select2-year-container").click()
        self.__pagina.get_by_role("option", name=str(ano)).click()

    def aplicar_filtros(self):
        """
        Aplica los filtros seleccionados en la página de estadísticas de las facturas creadas a clientes.
        """
        self.__pagina.locator("input[type='submit']").click()
        self.__pagina.wait_for_timeout(1000)

    def verificar_etiqueta_inexistente(self, etiqueta: str):
        """
        Verifica que una etiqueta no exista en la página de estadísticas de las facturas creadas a clientes.

        Args:
            etiqueta (str): Etiqueta a verificar.
        """
        assert (etiqueta is not None) and (len(etiqueta) > 0), "La etiqueta no puede estar vacía."
        self.__pagina.locator("input[class='select2-search__field']").fill(str(etiqueta))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")
    
    def verificar_tercero_inexistente(self, tercero: str):
        """
        Verifica que un tercero no exista en la página de estadísticas de las facturas creadas a clientes.

        Args:
            tercero (str): Tercero a verificar.
        """
        assert (tercero is not None) and (len(tercero) > 0), "El tercero no puede estar vacío."
        COMPONENTE = self.__pagina.locator("span[class='select2-selection select2-selection--single flat widthcentpercentminusx maxwidth300']").all()[0]
        COMPONENTE.click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(tercero))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_tipo_tercero_inexistente(self, tipo_tercero: str):
        """
        Verifica que un tipo de tercero no exista en la página de estadísticas de las facturas creadas a clientes.

        Args:
            tipo_tercero (str): Tipo de tercero a verificar.
        """
        assert (tipo_tercero is not None) and (len(tipo_tercero) > 0), "El tipo de tercero no puede estar vacío."
        self.__pagina.locator("#select2-typent_id-container").click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(tipo_tercero))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")
    
    def verificar_creador_inexistente(self, creador: str):
        """
        Verifica que un creador no exista en la página de estadísticas de las facturas creadas a clientes.

        Args:
            creador (str): Creador a verificar.
        """
        assert (creador is not None) and (len(creador) > 0), "El creador no puede estar vacío."
        self.__pagina.locator("#select2-userid-container").click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(creador))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_estado_inexistente(self, estado: str):
        """
        Verificar que un estado no exista en la página de estadísticas de las facturas creadas a clientes.
        
        Args:
            estado (str): Estado a verificar.
        """
        assert (estado is not None) and (len(estado) > 0), "El estado no puede estar vacío."
        self.__pagina.locator("#select2-object_status-container").click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(estado))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")
    
    def verificar_ano_inexistente(self, ano: str):
        """
        Verifica que un año no exista en la página de estadísticas de las facturas creadas a clientes.

        Args:
            ano (str): Año a verificar.
        """
        assert ano is not None, "El año no puede estar vacío."
        self.__pagina.locator("#select2-year-container").click()
        self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").fill(str(ano))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_filtros_aplicados(self,ano_inicial: str = ""):
        """
        Verifica que los filtros aplicados en la página de estadísticas de las facturas creadas a clientes sean correctos.

        Args:
            ano_inicial (str): Año inicial a verificar. Utilizarlo solo cuando no se aplique un filtro por año
        """
        if ano_inicial != "":
            expect(self.__pagina.get_by_role("link",name=ano_inicial)).to_be_visible()
        else:
            expect(self.__pagina.get_by_role("link",name=self.__ano)).to_be_visible()