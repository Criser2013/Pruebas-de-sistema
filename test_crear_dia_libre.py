from pages.LoginPage import LoginPage
from pages.CrearDiaLibrePage import CrearDiaLibrePage
from playwright.sync_api import Page, BrowserContext, Browser, expect
import pytest
from dotenv import load_dotenv
from os import getenv

load_dotenv()
URL = getenv("URL")

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, browser: Browser, context: BrowserContext):
    #Colocar cosas aquí que se ejecuten antes de cada test
    browser.new_context(locale="es-CO",timezone_id="America/Bogota")
    
    AUTH = LoginPage(URL, context)
    AUTH.ingresar_usuario(getenv("USUARIO"))
    AUTH.ingresar_contrasena(getenv("CONTRASENA"))
    AUTH.iniciar_sesion()
    AUTH.verificar_autenticacion()

    yield
    #colocar cosas aqui cuando termine el test
    context.close()

def test_crear_dia_usuario_valido(page: Page) -> None:
    PAGINA = CrearDiaLibrePage(page, URL)

    PAGINA.seleccionar_usuario("Juan Robles")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("06/04/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("בב")
    PAGINA.guardar_datos()

    PAGINA.verificar_guardado("test_crear_dia_libre")