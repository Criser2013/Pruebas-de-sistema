from pages.LoginPage import LoginPage
from pages.CrearFacturaProvPage import CrearFacturaProvPage
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
    Comprobando el guardado de una factura estándar - R1
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.seleccionar_tipo_factura("estandar")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.ingresar_ref_factura("Fact-001")
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_2(page: Page):
    """
    Comprobando el guardado de una factura de anticipo - R2
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.seleccionar_tipo_factura("anticipo")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.ingresar_ref_factura("Fact-002")
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_3(page: Page):
    """
    Comprobando que se muestre un error al no llenar el campo cliente - R3 y R5
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Proveedor' es obligatorio")
    PAGINA.verificar_error("El campo 'Referencia de factura del proveedor' es obligatorio")

def test_4(page: Page):
    """
    Comprobando que se mueste un error al no llenar el campo cliente y fecha - R4 y R6
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Proveedor' es obligatorio")
    PAGINA.verificar_error("El campo 'Fecha de la factura' es obligatorio")
    PAGINA.verificar_error("El campo 'Referencia de factura del proveedor' es obligatorio")

def test_5(page: Page):
    """
    Comprobando que se mueste un error al colocar una fecha futura - R7
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.seleccionar_tipo_factura("estandar")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.ingresar_ref_factura("Fact-003")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("Error, la fecha no puede ser futura")

def test_6(page: Page):
    """
    Comprobando que se guarde un abono - R8
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.ingresar_ref_factura("Fact-003")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="SI2505-0002 (Pagado)")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_7(page: Page):
    """
    Comprobando que se muestre un error al guardar un abono por colocar una fecha futura - R9
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.ingresar_ref_factura("Fact-004")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="SI2505-0002 (Pagado)")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("Error, la fecha no puede ser futura")

def test_8(page: Page):
    """
    Comprobando que se muestre un error al no seleccionar una factura a la cual abonar - R10
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="")
    PAGINA.ingresar_ref_factura("Fact-004")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Factura correcta ' es obligatorio")

def test_9(page: Page):
    """
    Comprobando que se muestre un error al ingresar una referencia ya utilizada - R11
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.seleccionar_proveedor("Proveedor pruebas")
    PAGINA.seleccionar_tipo_factura("estandar")
    PAGINA.ingresar_ref_factura("Fact-001")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("La referencia utilizada para la creación ya existe.")

def test_10(page: Page):
    """
    Comprobando que se muestre un error al no seleccionar un proveedor y usar una referencia existente - tiene un error :D - R12
    """
    PAGINA = CrearFacturaProvPage(page, URL)
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.ingresar_ref_factura("Fact-001")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Proveedor' es obligatorio")
    PAGINA.verificar_error("La referencia utilizada para la creación ya existe.")