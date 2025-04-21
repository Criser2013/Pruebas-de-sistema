from playwright.sync_api import BrowserContext, expect

class LoginPage:
    def __init__(self, url: str, context: BrowserContext) -> None:
        self.__usuario = "username"
        self.__contrasena = "password"
        self.__context = context
        self.__url = url

    def ingresar_usuario(self, usuario: str) -> None:
        self.__usuario = usuario

    def ingresar_contrasena(self, contrasena: str) -> None:
        self.__contrasena = contrasena

    def iniciar_sesion(self) -> None :
        page = self.__context.new_page()
        page.goto(self.__url)
        page.locator("input[id=username]").type(self.__usuario)
        page.locator("input[id=password]").type(self.__contrasena)
        page.locator("input[type=submit]").click()
        expect(page).to_have_title("Inicio - Dolibarr 15.0.3")
        page.close()