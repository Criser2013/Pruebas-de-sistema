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
    browser.new_context(locale="es-CO",timezone_id="America/Bogota")
    
    login_page = LoginPage(URL, context)
    login_page.ingresar_usuario(getenv("USUARIO"))
    login_page.ingresar_contrasena(getenv("CONTRASENA"))
    login_page.iniciar_sesion()
    yield
    #colocar cosas aqui cuando termine el test
    context.close()

def test_crear_dia_usuario_valido(page: Page) -> None:
    page.goto(f"{URL}/holiday/card.php?mainmenu=hrm&leftmenu=holiday&action=create")

    # Seleccionando el usuario 
    page.locator("span#select2-fuserid-container").click()
    page.get_by_role("option", name="Juan Robles").click()

    # Seleccionando el tipo de licencia
    page.locator("#select2-type-container").click()
    page.get_by_role("option", name="Baja por enfermedad").click()

    # Seleccionando la fecha de inicio
    page.locator("#date_debut_").fill("06/04/2025")
    page.locator("#select2-starthalfday-container").click()
    page.get_by_role("option", name="Mañana").click()

    # Seleccionando la fecha de fin
    page.locator("#date_fin_").fill("06/10/2025")
    page.locator("#select2-endhalfday-container").click()
    page.get_by_role("option", name="Tarde").click()

    # Seleccionando el revisor
    page.locator("span[id='select2-valideur-container']").click()
    page.get_by_role("option", name="Revisor Vacaciones").click()

    # Botón fuente HTML
    page.locator("#cke_46").click()

    # Colocando texto en la descripción (HTML)
    page.locator(
        "xpath=//textarea[@class='cke_source cke_reset cke_enable_context_menu cke_editable cke_editable_themed cke_contents_ltr']"
        ).fill("בב")

    # Clic en el botón de guardado
    page.get_by_role("button", name="Crear solicitud de licencia").click()
    
    # Verificando el guardado
    expect(page.get_by_text("Juan Robles")).to_be_visible()
    expect(page.get_by_text("Baja por enfermedad")).to_be_visible()
    expect(page.get_by_text("06/04/2025")).to_be_visible()
    expect(page.get_by_text("06/10/2025")).to_be_visible()
    expect(page.get_by_text("Revisor Vacaciones")).to_be_visible()
    expect(page.get_by_text("בב")).to_be_visible()

    # Verificando la marca de tiempo de grabación
    tiempo = page.locator("span[class=opacitymedium]").all()

    expect(tiempo[0]).to_contain_text("Mañana")
    expect(tiempo[1]).to_contain_text("Tarde")
    page.screenshot(path="screenshots/test_crear_dia_libre.png")