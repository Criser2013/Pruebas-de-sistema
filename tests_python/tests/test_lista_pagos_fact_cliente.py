from pages.LoginPage import LoginPage
from pages.ListaPagosClientePage import ListaPagosClientePage
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
    Filtrando por el campo "referencia de pago".
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("PAY2505-0001")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("308,88")

def test_2(page: Page):
    """
    Viendo todos los registros.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("1.106.350,74")

def test_3(page: Page):
    """
    Filtrando por una referencia de pago inexistente.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("PAY2505-1001")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_tabla_vacia()

def test_4(page: Page):
    """
    Filtrando por fecha de inicio.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("20/02/2025")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("1.106.350,74")

def test_5(page: Page):
    """
    Intentando filtrar por una fecha de inicio inválida.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("12321","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_error("El valor del campo 'Fecha de inicio'")

def test_6(page: Page):
    """
    Filtrando por fecha de fin.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","20/06/2025")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("1.106.350,74")

def test_7(page: Page):
    """
    Intentando filtrar por una fecha de fin inválida.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","1/12")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_error("El valor del campo 'Fecha de fin'")

def test_8(page: Page):
    """
    Filtrando por tercero.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("Cliente pruebas")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("1.105.550,74")

def test_9(page: Page):
    """
    Filtrando por tercero inexistente.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("Cliente que no existe")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_tabla_vacia()

def test_10(page: Page):
    """
    Filtrando por tipo de pago.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("Verificar")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("1.108,88")

def test_11(page: Page):
    """
    Filtrando por un tipo de pago inexistente.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.verificar_tipo_inexistente("Transferida")

def test_12(page: Page):
    """
    Filtrando por número de cheque/transferencia.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("CHEQUE-001")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("214.024,54")

def test_13(page: Page):
    """
    Filtrando por un número de cheque/transferencia inexistente.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("CHEU>ds1")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_tabla_vacia()

def test_14(page: Page):
    """
    Filtrando por cuenta bancaria.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("PAGOS-2")
    PAGINA.ingresar_importe("")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("891.217,32")

def test_15(page: Page):
    """
    Filtrando por una cuenta bancaria inexistente.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.ingresar_importe("")
    PAGINA.verificar_cuenta_inexistente("Cuenta inexistente")

def test_16(page: Page):
    """
    Filtrando por importe.
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe(">800")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_filtro("1.105.241,86")

def test_17(page: Page):
    """
    Filtrando por importe inválido. - tira error
    """
    PAGINA = ListaPagosClientePage(page, URL)
    PAGINA.ingresar_ref_pago("")
    PAGINA.ingresar_fecha("","")
    PAGINA.ingresar_tercero("")
    PAGINA.seleccionar_tipo_pago("")
    PAGINA.seleccionar_numero_cheque("")
    PAGINA.seleccionar_cuenta_bancaria("")
    PAGINA.ingresar_importe(";hola amigos_xd")
    PAGINA.aplicar_filtros()
    PAGINA.verificar_error("El valor del campo 'Importe' es inválido")