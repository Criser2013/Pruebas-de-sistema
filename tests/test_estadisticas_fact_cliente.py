from pages.LoginPage import LoginPage
from pages.EstadisticasFactClientePage import EstadisticasFactClientePage
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
    Comprobando que no se filtre por ninguna condición.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    ##PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_2(page: Page):
    """
    Filtrando con el campo "tercero".
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("Cliente pruebas")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_3(page: Page):
    """
    Intentando filtrar con un tercero inexistente.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_tercero_inexistente("Tercero imposible")

def test_4(page: Page):
    """
    Filtrando por el campo "tipo tercero".
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("Administración")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_5(page: Page):
    """
    Intentando filtrar con un tipo de tercero inexistente.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("Administración")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_6(page: Page):
    """
    Intentando filtrar con un tipo de tercero inexistente.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_tipo_tercero_inexistente("MyPYME")

def test_7(page: Page):
    """
    Filtrando con 2 etiquetas.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    PAGINA.seleccionar_etiqueta(("Preferente","Frecuente"))
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_8(page: Page):
    """
    Filtrando con una etiqueta.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    PAGINA.seleccionar_etiqueta("Frecuente")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_9(page: Page):
    """
    Intentando filtrar con una etiqueta inexistente.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("Administración")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_etiqueta_inexistente("Preferido")

def test_10(page: Page):
    """
    Filtrando por el campo "creador".
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("SuperAdmin")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_11(page: Page):
    """
    Intentando filtrar con un creador inexistente
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_estado("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_creador_inexistente("Creador Tickets")

def test_12(page: Page):
    """
    Filtrando por el campo "estado".
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("Borrador (necesita ser validado)")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_filtros_aplicados("2023")

def test_13(page: Page):
    """
    Intentando filtrar con un estado inexistente.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_ano("2025")
    PAGINA.verificar_estado_inexistente("Abonada")

def test_14(page: Page):
    """
    Intentando filtrar con un año vacío - falla :D
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.verificar_ano_inexistente("")

def test_15(page: Page):
    """
    Intentando filtrar con un año inexistente.
    """
    PAGINA = EstadisticasFactClientePage(page, URL)
    PAGINA.seleccionar_tercero("")
    PAGINA.seleccionar_tipo_tercero("")
    #PAGINA.seleccionar_etiqueta("")
    PAGINA.seleccionar_creador("")
    PAGINA.seleccionar_estado("")
    PAGINA.verificar_ano_inexistente("2026")