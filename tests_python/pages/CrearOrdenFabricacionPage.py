from re import sub
from playwright.sync_api import Page, expect

class  CrearOrdenFabricacionPage:

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina
        self.__pagina.goto(
            f"{url}/mrp/mo_card.php?leftmenu=mo&action=create")

    def seleccionar_tipo(self, tipo: str):
        self.__tipo = str(tipo)
        self.__pagina.locator("#select2-mrptype-container").click()
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

    def ingresar_fecha_inicio(self, fecha: str):
        self.__fecha_inicio = f"{str(fecha)}"
        self.__pagina.locator("#date_start_planned").fill(str(fecha))

    def ingresar_fecha_fin(self, fecha: str):
        self.__fecha_fin = f"{str(fecha)}"
        self.__pagina.locator("#date_end_planned").fill(str(fecha))

    def guardar_datos(self):
        self.__pagina.get_by_role("button", name="Crear").click()

    def verificar_error(self, texto: str):
        LOCATOR = self.__pagina.locator("div[class='jnotify-message']")
        expect(LOCATOR).to_be_visible()
        expect(LOCATOR).to_contain_text(str(texto))

    def verificar_guardado(self):
        expect(self.__pagina.get_by_role("cell",name=self.__tipo)).to_contain_text(self.__tipo)
        expect(self.__pagina.locator("td[class='valuefield fieldname_fk_product']")).to_contain_text(self.__producto)
        expect(self.__pagina.locator("td[class='valuefield fieldname_qty']")).to_contain_text(self.__cantidad)
        expect(self.__pagina.locator("td[class='valuefield fieldname_date_start_planned']")).to_contain_text(self.__fecha_inicio)
        expect(self.__pagina.locator("td[class='valuefield fieldname_date_end_planned']")).to_contain_text(self.__fecha_fin)

    def verificar_producto_inexistente(self, producto: str):
        self.__pagina.locator("#select2-fk_product-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[0].fill(str(producto))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_tipo_inexistente(self, tipo: str):
        self.__pagina.locator("#select2-bomtype-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[0].fill(str(tipo))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")