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

def test_1(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("Juan Robles")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("06/04/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("בב")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_1")

def test_2(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("Armando Casas")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("06/04/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("בב")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Usuario no disponible para solicitar días libres.")

def test_4(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("Juan Robles")
    PAGINA.seleccionar_tipo_dia_libre("Otro permiso")
    PAGINA.seleccionar_fecha_inicio("06/04/2024", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2024", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("בב")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_4")

def test_5(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("Juan Robles")
    PAGINA.seleccionar_fecha_inicio("06/04/2023", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2023", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("בב")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("El campo 'Tipo' es obligatorio")

def test_6(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("18/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("19/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_1")

def test_7(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("21/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("20/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_8(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("20/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_9(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("123456", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_10(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("2025/03/18", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_11(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("marzo 19 del 2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("06/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_12(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("18/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("20/10/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Ya se ha realizado una solicitud de licencia en este período.")

def test_13(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("22/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("24/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_13")

def test_14(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("25/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("21/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_15(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("25/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("26/03", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_16(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("25/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("26032025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_17(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("25/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("03/26/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("Debe seleccionar una fecha de finalización mayor que la fecha de inicio.")

def test_18(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("25/03/2025", "Mañana")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_fechas_no_selec(False)

def test_19(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("25/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("26/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_19")

def test_20(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("27/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("28/03/2025", "Tarde")
    PAGINA.verificar_revisor_no_existente("David Diaz")
    PAGINA.ingresar_descripcion("Descripción")
    page.screenshot(path="screenshots/test_20.png")

def test_21(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("27/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("28/03/2025", "Tarde")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_no_revisor("Debe elegir al aprobador para su solicitud de licencia.")
    page.screenshot(path="screenshots/test_20.png")

def test_22(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("27/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("28/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Hola 🥳")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_22")

def test_23(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("29/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("30/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("<h1>esto es html 🥳</h1>")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_23")

def test_24(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("27/03/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("28/03/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("OR TRUE;; DROP DATABASE dolidb;")
    PAGINA.guardar_datos()
    PAGINA.verificar_guardado("test_24")

def test_25(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_inicio("01/04/2025", "Mañana")
    PAGINA.seleccionar_fecha_fin("03/04/2025", "Tarde")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("a"*291)
    PAGINA.guardar_datos()
    PAGINA.verificar_error_modal("El campo 'Descripción' es muy largo.")

def test_26(page: Page):
    PAGINA = CrearDiaLibrePage(page, URL)
    PAGINA.seleccionar_usuario("David Diaz")
    PAGINA.seleccionar_tipo_dia_libre("Baja por enfermedad")
    PAGINA.seleccionar_fecha_fino("25/03/2025", "Mañana")
    PAGINA.seleccionar_revisor("Revisor Vacaciones")
    PAGINA.ingresar_descripcion("Descripción")
    PAGINA.guardar_datos()
    PAGINA.verificar_error_fechas_no_selec(True)