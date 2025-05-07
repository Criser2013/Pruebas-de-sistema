from pages.LoginPage import LoginPage
from pages.CrearListaMaterialesPage import CrearListaMaterialesPage
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
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_2(page: Page):
    """
    Caso 2
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("texto con emojis 😎😎")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_3(page: Page):
    """
    Caso 3
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Licuadora עברי")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_4(page: Page):
    """
    Caso 4
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("<html><h1>esto es HTML</h1></html>")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_5(page: Page):
    """
    Caso 5
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("a"*10000)
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'etiqueta' es demasiado largo.")

def test_6(page: Page):
    """
    Caso 6
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("' OR TRUE ;; DROP DATABASE 'postgres' ;")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'etiqueta' es inválido")

def test_7(page: Page):
    """
    Caso 7
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Etiqueta' es obligatorio")

def test_8(page: Page):
    """
    Caso 8
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.seleccionar_tipo("")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Tipo' es obligatorio")

def test_9(page: Page):
    """
    Caso 9
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.verificar_tipo_inexistente("Reconstrucción")

def test_10(page: Page):
    """
    Caso 10
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.verificar_producto_inexistente("Carro a control remoto")

def test_11(page: Page):
    """
    Caso 11
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Producto' es obligatorio")

def test_12(page: Page):
    """
    Caso 12
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El campo 'Cantidad' es obligatorio")

def test_13(page: Page):
    """
    Caso 13
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("-1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser positivo")

def test_14(page: Page):
    """
    Caso 14
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("10,92")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser un número entero positivo")

def test_15(page: Page):
    """
    Caso 15
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("hola :D")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Cantidad' debe ser un número entero positivo")

def test_16(page: Page):
    """
    Caso 16
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("texto con emojis 😎😎")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_17(page: Page):
    """
    Caso 17
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_18(page: Page):
    """
    Caso 18
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Licuadora עברי")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_19(page: Page):
    """
    Caso 19
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("<html><h1>esto es HTML</h1></html>")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_20(page: Page):
    """
    Caso 20
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("a"*10000)
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'descripción' es demasiado largo.")

def test_21(page: Page):
    """
    Caso 21
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("' OR TRUE ;; DROP DATABASE 'postgres' ;")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'descripción' es inválido.")

def test_22(page: Page):
    """
    Caso 22
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("", "")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_23(page: Page):
    """
    Caso 23
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("45", "00")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Duración' es inválido.")

def test_24(page: Page):
    """
    Caso 24
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("tex", "to")
    PAGINA.seleccionar_almacen("Zona franca 374")
    PAGINA.guardar_datos()
    PAGINA.verificar_error("El valor del campo 'Duración' es inválido.")

def test_25(page: Page):
    """
    Caso 25
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.seleccionar_almacen("")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado()

def test_26(page: Page):
    """
    Caso 26
    """
    PAGINA = CrearListaMaterialesPage(page, URL)
    PAGINA.ingresar_etiqueta("Materiales licuadora")
    PAGINA.ingresar_cantidad("1,00")
    PAGINA.seleccionar_tipo("Fabricación")
    PAGINA.seleccionar_producto("Licuadora Oster")
    PAGINA.ingresar_descripcion("Materiales para crear la licuadora")
    PAGINA.ingresar_duracion("01", "30")
    PAGINA.verificar_almacen_inexistente("Almacen Bogotá")