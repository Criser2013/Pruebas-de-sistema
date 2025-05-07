from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import unittest

class DolibarrArticuloTest(unittest.TestCase):
    """Test de caja negra usando tablas de decisión para la funcionalidad de crear un nuevo Artículo en Dolibarr"""

    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.driver = webdriver.Chrome()  
        self.driver.maximize_window()
        self.driver.get("http://localhost")  
        
        # Inicio de sesión
        self.login("admin", "admin")        
        self.navigate_to_new_article()

    def tearDown(self):
        """Acciones al finalizar cada prueba"""
        self.driver.quit()

    def login(self, username, password):
        """Función para iniciar sesión en Dolibarr"""
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        login_button.click()
        
        # Esperar a que cargue la página de inicio después de iniciar sesión
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id-left"))
        )

    def navigate_to_new_article(self):
        """Navega a la pantalla de creación de nuevo artículo"""
        # Navegar al módulo Base de Conocimientos
        knowledge_base_menu = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Base de Conocimientos')]"))
        )
        knowledge_base_menu.click()
        
        # Hacer clic en "Artículo nuevo"
        new_article_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Artículo nuevo')]"))
        )
        new_article_button.click()

    def fill_form(self, question=None, language=None, tags=None, solution=None):
        """Función para llenar el formulario según los parámetros dados"""
        # Llenar el campo Question si se proporciona
        if question is not None:
            question_field = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='question']")
            question_field.clear()
            question_field.send_keys(question)
        
        # Seleccionar idioma si se proporciona
        if language is not None:
            # Esperar a que el selector de idioma esté disponible
            language_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@name, 'lang')]"))
            )
            Select(language_select).select_by_visible_text(language)
        
        # Añadir etiquetas/categorías si se proporcionan
        if tags is not None:
            # Hacer clic en el campo de etiquetas para mostrar opciones
            tags_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='categories']")
            tags_field.click()
            
            # Seleccionar una etiqueta (esto puede variar según la implementación de Dolibarr)
            tag_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{tags}')]"))
            )
            tag_option.click()
        
        # Llenar solución si se proporciona
        if solution is not None:
            # Si el editor tiene un iframe
            try:
                self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, ".wysiwyg iframe"))
                solution_field = self.driver.find_element(By.CSS_SELECTOR, "body")
                solution_field.clear()
                solution_field.send_keys(solution)
                self.driver.switch_to.default_content()
            except NoSuchElementException:
                # Si es un textarea normal
                solution_field = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='solution']")
                solution_field.clear()
                solution_field.send_keys(solution)

    def submit_form(self):
        """Hacer clic en el botón CREAR para enviar el formulario"""
        create_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'CREAR')]")
        create_button.click()

    def check_for_error(self):
        """Comprueba si hay un mensaje de error en la página"""
        try:
            error_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".error, .errormessage"))
            )
            return True, error_message.text
        except TimeoutException:
            return False, None

    def check_for_success(self):
        """Comprueba si la creación fue exitosa"""
        try:
            # Buscar un mensaje de éxito o verificar si fuimos redirigidos a la lista de artículos
            success_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ok, .infomessage"))
            )
            return True
        except TimeoutException:
            # Verificar si estamos en la lista de artículos
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Lista de artículos')]"))
                )
                return True
            except TimeoutException:
                return False

    # CASOS DE PRUEBA

    def test_case_1(self):
        """CP1: Todos los campos completos (Question + Idioma + Etiquetas + Solution)"""
        self.fill_form(
            question="¿Cómo configurar usuarios en Dolibarr?",
            language="Árabe (Arabia Saudita)",
            tags="General",
            solution="Para configurar usuarios en Dolibarr, debe acceder al módulo de usuarios y completar el formulario correspondiente."
        )
        self.submit_form()
        
        # Verificar resultado esperado: creación exitosa
        self.assertTrue(self.check_for_success(), "No se creó el artículo con todos los campos")

    def test_case_2(self):
        """CP2: Solo campos obligatorios y etiquetas (Question + Idioma + Etiquetas)"""
        self.fill_form(
            question="¿Cuáles son los requisitos mínimos del sistema?",
            language="Árabe (Arabia Saudita)",
            tags="General"
        )
        self.submit_form()
        
        # Verificar resultado esperado: creación exitosa
        self.assertTrue(self.check_for_success(), "No se creó el artículo con campos obligatorios y etiquetas")

    def test_case_3(self):
        """CP3: Solo campos obligatorios (Question + Idioma)"""
        self.fill_form(
            question="¿Cómo instalar módulos adicionales?",
            language="Árabe (Arabia Saudita)"
        )
        self.submit_form()
        
        # Verificar resultado esperado: creación exitosa
        self.assertTrue(self.check_for_success(), "No se creó el artículo con solo campos obligatorios")

    def test_case_4(self):
        """CP4: Question completo, Idioma no seleccionado"""
        self.fill_form(
            question="¿Cómo exportar datos a Excel?"
        )
        self.submit_form()
        
        # Verificar resultado esperado: error por falta de idioma
        has_error, error_msg = self.check_for_error()
        self.assertTrue(has_error, "No se mostró error al faltar el campo obligatorio 'Idioma'")

    def test_case_5(self):
        """CP5: Question vacío, Idioma seleccionado"""
        self.fill_form(
            language="Árabe (Arabia Saudita)"
        )
        self.submit_form()
        
        # Verificar resultado esperado: error por falta de question
        has_error, error_msg = self.check_for_error()
        self.assertTrue(has_error, "No se mostró error al faltar el campo obligatorio 'Question'")

    def test_case_6(self):
        """CP6: Question completo, Idioma no seleccionado, con otros campos"""
        self.fill_form(
            question="¿Cómo importar contactos?",
            tags="General",
            solution="El proceso de importación de contactos requiere un archivo CSV..."
        )
        self.submit_form()
        
        # Verificar resultado esperado: error por falta de idioma
        has_error, error_msg = self.check_for_error()
        self.assertTrue(has_error, "No se mostró error al faltar el campo obligatorio 'Idioma' con otros campos llenos")

    def test_case_7(self):
        """CP7: Ambos campos obligatorios vacíos"""
        self.fill_form(
            tags="General",
            solution="Este es un texto de prueba para el cuerpo de la solución."
        )
        self.submit_form()
        
        # Verificar resultado esperado: error por falta de ambos campos
        has_error, error_msg = self.check_for_error()
        self.assertTrue(has_error, "No se mostró error al faltar ambos campos obligatorios")

    def test_case_8(self):
        """CP8: Question vacío pero con todos los demás campos completos"""
        self.fill_form(
            language="Árabe (Arabia Saudita)",
            tags="General",
            solution="Este es un texto de prueba detallado para la solución de un artículo en la base de conocimientos."
        )
        self.submit_form()
        
        # Verificar resultado esperado: error por falta de question
        has_error, error_msg = self.check_for_error()
        self.assertTrue(has_error, "No se mostró error al faltar Question con el resto de campos completos")


if __name__ == "__main__":
    unittest.main()
