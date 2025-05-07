from pages.LoginPage import LoginPage
from pages.CrearOrdenFabricacionPage import CrearOrdenFabricacionPage
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
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("")
    PAGINA.ingresar_fecha_fin("")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Tipo' es obligatorio")

def test_2(page: Page):
    """
    Caso 2
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("-1")
    PAGINA.ingresar_fecha_inicio("")
    PAGINA.ingresar_fecha_fin("")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser mayor o igual que 0.")
    PAGINA.verificar_error("El campo 'Tipo' es obligatorio")

def test_3(page: Page):
    """
    Caso 3
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("")
    PAGINA.seleccionar_tipo("")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/06/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Producto' es obligatorio")

def test_4(page: Page):
    """
    Caso 4
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("")
    PAGINA.seleccionar_tipo("")
    PAGINA.ingresar_cantidad("-1")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/06/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Producto' es obligatorio")
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser mayor o igual que 0.")

def test_5(page: Page):
    """
    Caso 5
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/04/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Producto' es obligatorio")
    PAGINA.verificar_error("La fecha de inicio debe ser superior a la fecha de finalización")

def test_6(page: Page):
    """
    Caso 6
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("-1")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/04/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Producto' es obligatorio")
    PAGINA.verificar_error("La fecha de inicio debe ser superior a la fecha de finalización")
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser mayor o igual que 0.")

def test_7(page: Page):
    """
    Caso 7
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/06/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Tipo' es obligatorio")

def test_8(page: Page):
    """
    Caso 8
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("")
    PAGINA.ingresar_fecha_fin("")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_9(page: Page):
    """
    Caso 9
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("-1")
    PAGINA.ingresar_fecha_inicio("")
    PAGINA.ingresar_fecha_fin("")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser mayor o igual que 0.")

def test_10(page: Page):
    """
    Caso 10
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/06/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_11(page: Page):
    """
    Caso 11
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("-1")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/06/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser mayor o igual que 0.")

def test_12(page: Page):
    """
    Caso 12
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("2")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/04/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("La fecha de inicio debe ser superior a la fecha de finalización")

def test_13(page: Page):
    """
    Caso 13
    """
    PAGINA = CrearOrdenFabricacionPage(page, URL)
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_cantidad("-1")
    PAGINA.ingresar_fecha_inicio("26/05/2025")
    PAGINA.ingresar_fecha_fin("26/04/2025")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser mayor o igual que 0.")
    PAGINA.verificar_error("La fecha de inicio debe ser superior a la fecha de finalización")