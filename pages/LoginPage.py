from playwright.sync_api import BrowserContext, expect

class LoginPage:
    """
    Clase que representa la página de inicio de sesión. Posee métodos para interactuar
    con el formulario de inicio de sesión y verificar la autenticación.
    """

    def __init__(self, url: str, context: BrowserContext) -> None:
        self.__usuario = ""
        self.__contrasena = ""
        self.__context = context
        self.__url = str(url)
        self.__pagina = self.__context.new_page()
        self.__pagina.goto(self.__url)

    def ingresar_usuario(self, usuario: str) -> None:
        """
        Ingresa el nombre de usuario en el campo correspondiente.

        Args:
            usuario (str): Nombre de usuario para iniciar sesión.
        """
        if len(usuario) > 0:
            self.__usuario = str(usuario)
            self.__pagina.locator("input[id=username]").type(self.__usuario)
        else:
            raise Exception("El usuario no puede estar vacío.")

    def ingresar_contrasena(self, contrasena: str) -> None:
        """
        Ingresa la contraseña en el campo correspondiente.

        Args:
            contrasena (str): Contraseña del usuario.
        """
        if len(contrasena) > 0:
            self.__contrasena = str(contrasena)
            self.__pagina.locator("input[id=password]").type(self.__contrasena)
        else:
            raise Exception("La contraseña no puede estar vacía.")

    def iniciar_sesion(self) -> None :
        """
        Inicia sesión en la aplicación haciendo clic en el botón de inicio de sesión.
        """
        self.__pagina.locator("input[type=submit]").click()

    def verificar_autenticacion(self):
        """
        Verifica si la autenticación fue exitosa al comprobar el título de la página.
        """
        expect(self.__pagina).to_have_title("Inicio - Dolibarr 21.0.1")
        self.__pagina.close()