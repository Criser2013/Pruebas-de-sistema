import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

class DolibarrNewBudgetTest(unittest.TestCase):
    """
    Clase para automatizar las pruebas de la funcionalidad 'Nuevo presupuesto' en Dolibarr.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada caso de prueba
        """
        # Inicializar el controlador del navegador (Chrome)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
        # URL de la aplicación Dolibarr
        self.base_url = "http://localhost"
        
        # Credenciales de inicio de sesión
        self.username = "admin"
        self.password = "admin"
        
        # Iniciar sesión en Dolibarr
        self.login()
        
    def tearDown(self):
        """
        Limpieza después de cada caso de prueba
        """
        # Cerrar el navegador
        self.driver.quit()
        
    def login(self):
        """
        Método para iniciar sesión en Dolibarr
        """
        # Navegar a la página de inicio de sesión
        self.driver.get(self.base_url)
        
        # Esperar a que la página de inicio de sesión se cargue
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Introducir credenciales y hacer clic en el botón de inicio de sesión
        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # Esperar a que la página principal se cargue
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id-left"))
        )
    
    def navigate_to_new_budget(self):
        """
        Navegar a la página de creación de nuevo presupuesto
        """
        # Hacer clic en el menú Presupuestos
        self.driver.find_element(By.XPATH, "//a[contains(text(), 'Presupuestos')]").click()
        
        # Esperar y hacer clic en Nuevo presupuesto
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Nuevo presupuesto')]"))
        ).click()
        
        # Esperar a que se cargue la página de nuevo presupuesto
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Nuevo presupuesto')]"))
        )
    
    def select_provider(self, select=True, provider_name="Mi Proveedor"):
        """
        Seleccionar o no un proveedor según el parámetro select
        """
        if select:
            # Hacer clic en el selector de proveedor
            self.driver.find_element(By.XPATH, "//span[contains(@class, 'select2-selection')]").click()
            
            # Esperar a que aparezca el desplegable y seleccionar el proveedor
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']"))
            ).send_keys(provider_name)
            
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'select2-results__option')]"))
            ).click()
    
    def select_payment_conditions(self, select=True, condition="30 días"):
        """
        Seleccionar o no condiciones de pago
        """
        if select:
            # Localizar y seleccionar las condiciones de pago
            payment_conditions = Select(self.driver.find_element(By.NAME, "cond_reglement_id"))
            payment_conditions.select_by_visible_text(condition)
    
    def select_payment_form(self, select=True, form="Transferencia bancaria"):
        """
        Seleccionar o no una forma de pago
        """
        if select:
            # Hacer clic en el selector de forma de pago
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'form-group')]//span[contains(@id, 'select2-mode_reglement')]").click()
            
            # Esperar y seleccionar la forma de pago
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[text()='{form}']"))
            ).click()
    
    def select_shipping_method(self, select=True, method="Generic transport service"):
        """
        Seleccionar o no un método de envío
        """
        if select:
            # Hacer clic en el selector de método de envío
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'form-group')]//span[contains(@id, 'select2-shipping_method')]").click()
            
            # Esperar y seleccionar el método de envío
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[text()='{method}']"))
            ).click()
    
    def set_delivery_date(self, valid=True, use_now=False):
        """
        Establecer la fecha de entrega
        """
        if use_now:
            # Hacer clic en el botón 'Ahora'
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Ahora')]").click()
        elif valid:
            # Establecer una fecha válida en el futuro (1 mes después)
            self.driver.find_element(By.NAME, "date_livraison").clear()
            self.driver.find_element(By.NAME, "date_livraison").send_keys("05/06/2025")
        else:
            # Establecer una fecha inválida
            self.driver.find_element(By.NAME, "date_livraison").clear()
            self.driver.find_element(By.NAME, "date_livraison").send_keys("31/02/2025")
    
    def select_default_template(self, select=True, template="aurore"):
        """
        Seleccionar o no una plantilla por defecto
        """
        if select:
            # Seleccionar la plantilla por defecto
            template_select = Select(self.driver.find_element(By.NAME, "model"))
            template_select.select_by_visible_text(template)
    
    def select_project(self, select=True, project="Proyecto Principal"):
        """
        Seleccionar o no un proyecto
        """
        if select:
            # Hacer clic en el selector de proyecto
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'form-group')]//span[contains(@id, 'select2-projectid')]").click()
            
            # Esperar y seleccionar el proyecto
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{project}')]"))
            ).click()
    
    def select_currency(self, select=True, currency="€"):
        """
        Seleccionar o no una divisa
        """
        if select:
            # Seleccionar la divisa
            currency_select = Select(self.driver.find_element(By.NAME, "multicurrency_code"))
            currency_select.select_by_visible_text(currency)
    
    def click_create_draft(self):
        """
        Hacer clic en el botón 'CREAR BORRADOR'
        """
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR BORRADOR')]").click()
    
    def check_error_message(self):
        """
        Verificar si se muestra un mensaje de error
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error"))
            )
            return True
        except TimeoutException:
            return False
    
    def check_success_message(self):
        """
        Verificar si se muestra un mensaje de éxito
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ok"))
            )
            return True
        except TimeoutException:
            return False

    # CASOS DE PRUEBA
    
    def test_CP1_all_fields_valid(self):
        """
        CP1: Caso válido con todos los campos correctos
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions()
        self.select_payment_form()
        self.select_shipping_method()
        self.set_delivery_date()
        self.select_default_template()
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se creó correctamente (mensaje de éxito o redirección)
        self.assertTrue(self.check_success_message())
    
    def test_CP2_no_provider(self):
        """
        CP2: Caso sin proveedor seleccionado
        """
        self.navigate_to_new_budget()
        
        self.select_provider(select=False)
        self.select_payment_conditions()
        self.select_payment_form()
        self.select_shipping_method()
        self.set_delivery_date()
        self.select_default_template()
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se muestra un mensaje de error
        self.assertTrue(self.check_error_message())
    
    def test_CP3_no_payment_conditions(self):
        """
        CP3: Caso sin condiciones de pago seleccionadas
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions(select=False)
        self.select_payment_form()
        self.select_shipping_method()
        self.set_delivery_date()
        self.select_default_template()
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se muestra un mensaje de error
        self.assertTrue(self.check_error_message())
    
    def test_CP4_no_payment_form(self):
        """
        CP4: Caso sin forma de pago seleccionada
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions()
        self.select_payment_form(select=False)
        self.select_shipping_method()
        self.set_delivery_date()
        self.select_default_template()
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se muestra un mensaje de error
        self.assertTrue(self.check_error_message())
    
    def test_CP5_no_shipping_method(self):
        """
        CP5: Caso sin método de envío seleccionado
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions()
        self.select_payment_form()
        self.select_shipping_method(select=False)
        self.set_delivery_date()
        self.select_default_template()
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se muestra un mensaje de error
        self.assertTrue(self.check_error_message())
    
    def test_CP6_invalid_delivery_date(self):
        """
        CP6: Caso con fecha de entrega inválida
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions()
        self.select_payment_form()
        self.select_shipping_method()
        self.set_delivery_date(valid=False)
        self.select_default_template()
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se creó correctamente (pero sin fecha)
        self.assertTrue(self.check_success_message())
    
    def test_CP7_no_default_template(self):
        """
        CP7: Caso sin plantilla por defecto
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions()
        self.select_payment_form()
        self.select_shipping_method()
        self.set_delivery_date(use_now=True)
        self.select_default_template(select=False)
        self.select_project()
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se creó correctamente
        self.assertTrue(self.check_success_message())
    
    def test_CP8_no_project(self):
        """
        CP8: Caso sin proyecto seleccionado
        """
        self.navigate_to_new_budget()
        
        self.select_provider()
        self.select_payment_conditions()
        self.select_payment_form()
        self.select_shipping_method()
        self.set_delivery_date()
        self.select_default_template()
        self.select_project(select=False)
        self.select_currency()
        
        self.click_create_draft()
        
        # Verificar que se creó correctamente
        self.assertTrue(self.check_success_message())

if __name__ == "__main__":
    unittest.main()
