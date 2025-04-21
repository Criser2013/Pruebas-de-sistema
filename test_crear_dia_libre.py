from pages.LoginPage import LoginPage
from playwright.sync_api import Page, BrowserContext, Browser, expect
import pytest
from dotenv import load_dotenv
from os import getenv

load_dotenv()
URL = getenv("URL")

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, browser: Browser, context: BrowserContext):
    #Colocar cosas aquí que se ejecuten antes de cada test
    browser.new_context(locale="es-ES")
    login_page = LoginPage(URL, context)
    login_page.ingresar_usuario(getenv("USUARIO"))
    login_page.ingresar_contrasena(getenv("CONTRASENA"))
    login_page.iniciar_sesion()
    yield
    browser.close()
    #Colocar cosas aquí que se ejecuten despues de cada test

def test_crear_dia_usuario_valido(page: Page) -> None:
    page.goto(f"{URL}/holiday/card.php?mainmenu=hrm&leftmenu=holiday&action=create")
    # Click the get started link.