from pages.LoginPage import LoginPage
from pages.CrearFacturaClientePage import CrearFacturaClientePage
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
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("estandar")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_2(page: Page):
    """
    Comprobando el guardado de una factura de anticipo - hay un error :D - R2
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("anticipo")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_3(page: Page):
    """
    Comprobando que se muestre un error al no llenar el campo cliente - R3 y R5
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Cliente' es obligatorio")

def test_4(page: Page):
    """
    Comprobando que se mueste un error al no llenar el campo cliente y fecha - R4 y R6
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Cliente' es obligatorio")
    PAGINA.verificar_error("El campo 'Fecha' es obligatorio")

def test_5(page: Page):
    """
    Comprobando que se mueste un error al colocar una fecha futura - R7
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("estandar")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("Error, la fecha no puede ser futura")


def test_6(page: Page):
    """
    Comprobando que se guarde una factura rectificativa - R8
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("rectificativa",factura_rectificativa="IN2505-0004 (No pagado)")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_7(page: Page):
    """
    Comprobando que se muestre un error al guardar una factura rectificativa y colocar una fecha futura - R9
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("rectificativa",factura_rectificativa="IN2505-0004 (No pagado)")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("Error, la fecha no puede ser futura")

def test_8(page: Page):
    """
    Comprobando que se muestre un error al no seleccionar una factura rectificativa - R10
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("rectificativa",factura_rectificativa="")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Reemplazar factura ' es obligatorio")

def test_9(page: Page):
    """
    Comprobando que se muestre un error al no seleccionar una factura rectificativa y colocar una fecha futura - R11
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("rectificativa",factura_rectificativa="")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Reemplazar factura ' es obligatorio")
    PAGINA.verificar_error("Error, la fecha no puede ser futura")

def test_10(page: Page):
    """
    Comprobando el guardado de una factura de abono - tiene un error :D - R12
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="IN2505-0001 (Pagado)")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_guardado()

def test_11(page: Page):
    """
    Comprobando que se muestre un error al colocar una fecha futura - R13
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="IN2505-0001 (Pagado)")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("Error, la fecha no puede ser futura")

def test_12(page: Page):
    """
    Comprobando que se muestre un error al no seleccionar una factura pagada o pendiente por pagar - R14
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="")
    PAGINA.ingresar_fecha_factura(hoy=True)
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Factura correcta ' es obligatorio")

def test_13(page: Page):
    """
    Comprobando que se muestre un error al colocar una fecha futura y no seleccionar una factura pagada o pendiente por pagar - R15
    """
    PAGINA = CrearFacturaClientePage(page, URL)
    PAGINA.seleccionar_cliente("Cliente pruebas")
    PAGINA.seleccionar_tipo_factura("abono",factura_abono="")
    PAGINA.ingresar_fecha_factura("01/06/2025")
    PAGINA.seleccionar_condicion_pago("30 días de fin de mes")
    PAGINA.guardar_factura()
    PAGINA.verificar_error("El campo 'Factura correcta ' es obligatorio")
    PAGINA.verificar_error("Error, la fecha no puede ser futura")