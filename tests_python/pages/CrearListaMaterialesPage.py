from re import sub
from playwright.sync_api import Page, expect, Dialog

class  CrearListaMaterialesPage:

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina
        self.__pagina.goto(
            f"{url}/bom/bom_card.php?leftmenu=bom&action=create")

    def ingresar_etiqueta(self, etiqueta: str):
        self.__etiqueta = self.__limpiar_html(str(etiqueta))
        self.__pagina.locator("#label").fill(str(etiqueta))

    def seleccionar_tipo(self, tipo: str):
        self.__tipo = str(tipo)
        self.__pagina.locator("#select2-bomtype-container").click()
        if tipo == "":
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(tipo)).click()

    def seleccionar_producto(self, producto: str):
        self.__producto = str(producto).replace(" ", "_")
        self.__pagina.locator("#select2-fk_product-container").click()

        if producto == "":
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            AUX = self.__producto.replace(" ", "_")
            self.__pagina.get_by_role("option", name=f"{AUX} - {str(producto)}").click()

    def ingresar_cantidad(self, cantidad: str):
        self.__cantidad = str(cantidad)
        self.__pagina.locator("#qty").fill(str(cantidad))

    def ingresar_descripcion(self, descripcion: str):
        self.__descripcion = self.__limpiar_html(str(descripcion))
        self.__pagina.locator("#description").fill(str(descripcion))

    def ingresar_duracion(self, horas: str, minutos: str):
        self.__duracion = f"{str(horas)}:{str(minutos)}" if horas != "" and minutos != "" else ""
        self.__pagina.locator("input[name='durationhour']").fill(str(horas))
        self.__pagina.locator("input[name='durationmin']").fill(str(minutos))

    def seleccionar_almacen(self, almacen: str):
        self.__almacen = str(almacen)
        self.__pagina.locator("#select2-fk_warehouse-container").click()

        if almacen == "":
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(almacen)).click()

    def guardar_datos(self):
        self.__pagina.get_by_role("button", name="Crear").click()

    def verificar_error(self, texto: str):
        LOCATOR = self.__pagina.locator("div[class='jnotify-message']")
        expect(LOCATOR).to_be_visible()
        expect(LOCATOR).to_contain_text(str(texto))

    def verificar_guardado(self):
        expect(self.__pagina.get_by_role("cell",name=self.__etiqueta)).to_contain_text(self.__etiqueta)
        expect(self.__pagina.get_by_role("cell",name=self.__tipo).all()[0]).to_contain_text(self.__tipo)        
        expect(self.__pagina.get_by_role("cell",name=self.__producto)).to_contain_text(self.__producto)
        expect(self.__pagina.get_by_role("cell",name=self.__cantidad)).to_contain_text(self.__cantidad)
        expect(self.__pagina.locator(".longmessagecut")).to_contain_text(self.__descripcion)
        expect(self.__pagina.locator("td[class='valuefield fieldname_duration']")).to_contain_text(self.__duracion)
        expect(self.__pagina.locator("td[class='valuefield fieldname_fk_warehouse']")).to_contain_text(self.__almacen)

    def verificar_producto_inexistente(self, producto: str):
        self.__pagina.locator("#select2-fk_product-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[0].fill(str(producto))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_almacen_inexistente(self, almacen: str):
        self.__pagina.locator("#select2-fk_warehouse-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[0].fill(str(almacen))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_tipo_inexistente(self, tipo: str):
        self.__pagina.locator("#select2-bomtype-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[0].fill(str(tipo))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def __limpiar_html(self, texto: str) -> str:
        """
        Elimina todas las etiquetas HTML de una cadena de texto.
        
        Args:
            texto (str): Texto que contiene etiquetas HTML.
            
        Return:
            str: Texto sin etiquetas HTML.
        """
        return sub(r'<[^>]+>', '', texto)