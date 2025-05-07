from re import sub
from playwright.sync_api import Page, expect, Dialog

class  CrearArticuloPage:

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina
        self.__pagina.goto(
            f"{url}/knowledgemanagement/knowledgerecord_card.php?action=create&idmenu=32&mainmenu=ticket&leftmenu=")

    def ingresar_pregunta(self, pregunta: str):
        self.__pregunta = self.__limpiar_html(str(pregunta))
        self.__pagina.locator("#question").fill(str(pregunta))

    def seleccionar_idioma(self, idioma: str, opcion: str):
        self.__idioma = str(idioma)
        self.__pagina.locator("#select2-lang-container").click()

        if idioma == "":
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(opcion)).click()

    def seleccionar_etiqueta(self,etiqueta: str|tuple):
        self.__etiquetas = etiqueta
        if isinstance(etiqueta, tuple):
            for i in etiqueta:
                self.__pagina.locator("ul[class=select2-selection__rendered]").click()
                self.__pagina.get_by_role("option", name=str(i)).click()
        elif etiqueta != "":
            self.__pagina.locator("ul[class=select2-selection__rendered]").click()
            self.__pagina.get_by_role("option", name=str(etiqueta)).click()

    def seleccionar_sugerido(self, sugerido: str):
        self.__pagina.locator("#select2-fk_c_ticket_category-container").click()
        self.__sugerido = str(sugerido)

        if sugerido == "":
            self.__pagina.locator("xpath=//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']").press("Enter")
        else:
            self.__pagina.get_by_role("option", name=str(sugerido)).click()

    def ingresar_solucion(self, solucion: str):
        self.__solucion = str(solucion)
        self.__pagina.get_by_role("button",name="Fuente HTML").click()
        self.__pagina.get_by_role("textbox", name="Editor de Texto Enriquecido, answer").fill(str(solucion))
    
    def guardar_datos(self):
        self.__pagina.get_by_role("button", name="Crear").click()

    def verificar_error(self, texto: str):
        LOCATOR = self.__pagina.locator("div[class='jnotify-message']")
        expect(LOCATOR).to_be_visible()
        expect(LOCATOR).to_contain_text(str(texto))

    def verificar_guardado(self):
        expect(self.__pagina.locator(".longmessagecut")).to_contain_text(self.__pregunta)
        expect(self.__pagina.locator("td[class='valuefield fieldname_lang']")).to_contain_text(self.__idioma)
        expect(self.__pagina.locator("td[class='valuefield fieldname_fk_c_ticket_category']")).to_contain_text(self.__sugerido)

        if isinstance(self.__etiquetas, tuple):
            for i in self.__etiquetas:
                expect(self.__pagina.get_by_role("link", name=str(i))).to_be_visible()
        elif self.__etiquetas != "":
            expect(self.__pagina.get_by_role("link", name=str(self.__etiquetas))).to_be_visible()

        self.__pagina.get_by_role("button",name="Fuente HTML").click()
        expect(self.__pagina.locator("#answer")).to_contain_text(self.__solucion)
        #expect(self.__pagina.get_by_role("textbox", name="Editor de Texto Enriquecido, answer")).to_contain_text(self.__solucion)

    def verificar_idioma_inexistente(self, idioma: str):
        self.__pagina.locator("#select2-lang-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[0].fill(str(idioma))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_sugerido_inexistente(self, sugerido: str):
        self.__pagina.locator("#select2-fk_c_ticket_category-container").click()
        self.__pagina.locator("input[class='select2-search__field']").all()[1].fill(str(sugerido))
        expect(self.__pagina.locator("li[class='select2-results__option select2-results__message']")).to_have_text("No se han encontrado resultados")

    def verificar_etiqueta_inexistente(self, etiqueta: str):
        self.__pagina.locator("input[class='select2-search__field']").fill(str(etiqueta))
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