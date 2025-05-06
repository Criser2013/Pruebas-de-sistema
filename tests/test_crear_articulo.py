from pages.LoginPage import LoginPage
from pages.CrearArticuloPage import CrearArticuloPage
from playwright.sync_api import Page, BrowserContext, Browser
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

def test_1(page: Page):
    """
    Caso 1
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_2(page: Page):
    """
    Caso 2
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("<html><h1>esto es HTML</h1></html>")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_3(page: Page):
    """
    Caso 3
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("texto con emojis 😎😎")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_4(page: Page):
    """
    Caso 4
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Esto es HTML עברי")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_5(page: Page):
    """
    Caso 5
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Question' es obligatorio")

def test_6(page: Page):
    """
    Caso 6
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("a"*10000)
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Question' es demasiado largo")

def test_7(page: Page):
    """
    Caso 7
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta(" OR TRUE ;; DROP DATABASE 'postgres' ;")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'solution' es inválido")

def test_8(page: Page):
    """
    Caso 8
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("","")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_9(page: Page):
    """
    Caso 9
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("","")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.verificar_idioma_inexistente("Idioma 😀 123232 עברי")

def test_10(page: Page):
    """
    Caso 10
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.verificar_sugerido_inexistente("123213 עברי 😀")

def test_11(page: Page):
    """
    Caso 11
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta("")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_12(page: Page):
    """
    Caso 12
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta(("Importante","Requerido"))
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_13(page: Page):
    """
    Caso 13
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.ingresar_solucion("Adiós")
    PAGINA.verificar_etiqueta_inexistente("Difícil")

def test_14(page: Page):
    """
    Caso 14
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.ingresar_solucion("<html><h1>esto es HTML</h1></html>")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_15(page: Page):
    """
    Caso 15
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.ingresar_solucion("texto con emojis 😎😎")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_16(page: Page):
    """
    Caso 16
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.ingresar_solucion("Esto es HTML עברי")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_17(page: Page):
    """
    Caso 17
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.ingresar_solucion(" OR TRUE ;; DROP DATABASE 'postgres' ;")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'solution' es inválido")

def test_18(page: Page):
    """
    Caso 18
    """
    PAGINA = CrearArticuloPage(page, URL)
    PAGINA.ingresar_pregunta("Hola")
    PAGINA.seleccionar_idioma("Español (Colombia)","Español (Colombia) (es_CO)")
    PAGINA.seleccionar_sugerido("Other")
    PAGINA.seleccionar_etiqueta("Importante")
    PAGINA.ingresar_solucion("a"*10000)
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Question' es demasiado largo")