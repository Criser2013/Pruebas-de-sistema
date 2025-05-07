import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class DolibarrTicketsTest(unittest.TestCase):
    
    def setUp(self):
        # Inicializar el navegador
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        
        self.base_url = "http://127.0.0.1/ticket/index.php?mainmenu=ticket&leftmenu="
        
        # Iniciar sesión en Dolibarr
        self.login()
    
    def login(self):
        """Método para iniciar sesión en Dolibarr"""
        self.driver.get(f"{self.base_url}/dolibarr/index.php")
        
        # Esperar a que cargue la página de login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Ingresar credenciales (usar las credenciales de tu instalación)
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        
        # Esperar a que cargue la página principal
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'mainmenu')]"))
        )
    
    def navigate_to_tickets(self):
        """Navegar a la sección de tickets"""
        # Clic en el menú de Tickets
        self.driver.get(f"{self.base_url}/dolibarr/ticket/list.php")
        
        # Esperar a que cargue la lista de tickets
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'liste')]"))
        )
    
    def clear_all_filters(self):
        """Limpiar todos los filtros existentes"""
        try:
            # Verificar si existe el botón para limpiar filtros y hacer clic en él
            clear_button = self.driver.find_element(By.XPATH, "//input[@value='Borrar filtro']")
            clear_button.click()
            time.sleep(1)  # Esperar a que se aplique la limpieza
        except NoSuchElementException:
            # No hay filtros que limpiar o el botón no está presente
            pass
    
    def verify_results(self, expected_condition, error_message):
        """Verificar los resultados basado en una condición esperada"""
        try:
            # Esperar a que se actualice la tabla después de aplicar filtros
            WebDriverWait(self.driver, 5).until(expected_condition)
            return True
        except TimeoutException:
            self.fail(error_message)
            return False
    
    def count_visible_rows(self):
        """Contar el número de filas visibles en la tabla de resultados"""
        rows = self.driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[not(contains(@style, 'display: none'))]")
        # Restar 1 para excluir la fila de encabezado si es necesario
        return len(rows) - 1 if len(rows) > 0 else 0
    
    # CASOS DE PRUEBA
    
    def test_CP1_filter_by_existing_reference(self):
        """CP1: Filtrar por referencia existente"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Ingresa la referencia en el campo de filtro
        ref_input = self.driver.find_element(By.XPATH, "//input[@name='search_ref']")
        ref_input.clear()
        ref_input.send_keys("TS2505-0004")
        ref_input.send_keys(Keys.RETURN)
        
        # Verificar que solo se muestra el ticket con la referencia especificada
        def check_condition(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr")
            if len(rows) < 2:  # Si solo hay una fila (encabezado), no se encontraron resultados
                return False
            # Verificar que la referencia del ticket mostrado coincide
            ref_cell = driver.find_element(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[2]/td[contains(@class, 'ref')]")
            return "TS2505-0004" in ref_cell.text
        
        self.verify_results(
            expected_condition=check_condition,
            error_message="No se encontró el ticket con la referencia especificada"
        )
    
    def test_CP2_filter_by_nonexistent_reference(self):
        """CP2: Filtrar por referencia inexistente"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Ingresa una referencia inexistente
        ref_input = self.driver.find_element(By.XPATH, "//input[@name='search_ref']")
        ref_input.clear()
        ref_input.send_keys("REF-99999")
        ref_input.send_keys(Keys.RETURN)
        
        # Verificar que no se muestran resultados
        def check_no_results(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr")
            # Si solo hay una fila (encabezado) o hay un mensaje de "No se encontraron resultados"
            return len(rows) <= 1 or driver.find_element(By.XPATH, "//*[contains(text(), 'No se encontraron resultados')]")
        
        self.verify_results(
            expected_condition=check_no_results,
            error_message="Se encontraron resultados cuando no debería haberlos"
        )
    
    def test_CP5_filter_by_high_severity(self):
        """CP5: Filtrar por gravedad Alta"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Seleccionar gravedad Alta
        try:
            # Intentar encontrar un dropdown de gravedad
            severity_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_severity_id']"))
            severity_select.select_by_visible_text("Alto")
        except NoSuchElementException:
            # Si no es un dropdown, puede ser una lista desplegable al hacer clic
            severity_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Gravedad')]")
            severity_button.click()
            # Esperar a que aparezca el menú desplegable
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            # Seleccionar "Alto"
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='Alto']").click()
        
        # Verificar que solo se muestran tickets con gravedad Alta
        def check_severity(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[position() > 1]")
            if len(rows) == 0:
                return False
            
            for row in rows:
                severity_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'severity') or contains(text(), 'Alto')]")
                if "Alto" not in severity_cell.text:
                    return False
            return True
        
        self.verify_results(
            expected_condition=check_severity,
            error_message="Se muestran tickets que no tienen gravedad Alta"
        )
    
    def test_CP12_filter_by_progress(self):
        """CP12: Filtrar por progreso específico"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Ingresar el valor de progreso
        progress_input = self.driver.find_element(By.XPATH, "//input[@name='search_progress']")
        progress_input.clear()
        progress_input.send_keys("100")
        progress_input.send_keys(Keys.RETURN)
        
        # Verificar que solo se muestran tickets con 100% de progreso
        def check_progress(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[position() > 1]")
            if len(rows) == 0:
                return False
            
            for row in rows:
                progress_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'progress') or contains(text(), '100')]")
                if "100" not in progress_cell.text:
                    return False
            return True
        
        self.verify_results(
            expected_condition=check_progress,
            error_message="Se muestran tickets que no tienen 100% de progreso"
        )
    
    def test_CP13_filter_by_invalid_progress(self):
        """CP13: Intentar filtrar por valor no numérico en Progreso"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Ingresar un valor no numérico
        progress_input = self.driver.find_element(By.XPATH, "//input[@name='search_progress']")
        progress_input.clear()
        progress_input.send_keys("abc")
        progress_input.send_keys(Keys.RETURN)
        
        # Verificar que el sistema maneja adecuadamente el valor inválido
        # Esto podría ser un mensaje de error o simplemente no mostrar resultados
        def check_error_handling(driver):
            # Buscar un mensaje de error o verificar que no haya cambios significativos
            try:
                error_message = driver.find_element(By.XPATH, "//*[contains(@class, 'error') or contains(text(), 'error')]")
                return True
            except NoSuchElementException:
                # Si no hay mensaje de error, verificar que la entrada no es aceptada o es ignorada
                current_value = driver.find_element(By.XPATH, "//input[@name='search_progress']").get_attribute("value")
                return current_value == "" or current_value != "abc"
        
        self.verify_results(
            expected_condition=check_error_handling,
            error_message="El sistema no manejó adecuadamente el valor no numérico"
        )
    
    def test_CP14_filter_by_resolved_status(self):
        """CP14: Filtrar por estado Resuelto"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Seleccionar estado Resuelto
        try:
            # Intentar encontrar un dropdown de estado
            status_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_fk_status']"))
            status_select.select_by_visible_text("Resuelto")
        except NoSuchElementException:
            # Si no es un dropdown, puede ser una lista desplegable al hacer clic
            status_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Estado')]")
            status_button.click()
            # Esperar a que aparezca el menú desplegable
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            # Seleccionar "Resuelto"
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='Resuelto']").click()
        
        # Verificar que solo se muestran tickets con estado Resuelto
        def check_status(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[position() > 1]")
            if len(rows) == 0:
                return False
            
            for row in rows:
                status_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'status') or contains(text(), 'Resuelto')]")
                if "Resuelto" not in status_cell.text:
                    return False
            return True
        
        self.verify_results(
            expected_condition=check_status,
            error_message="Se muestran tickets que no tienen estado Resuelto"
        )
    
    def test_CP16_filter_by_multiple_criteria(self):
        """CP16: Filtrar por múltiples criterios (Estado + Gravedad)"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Seleccionar estado Resuelto
        try:
            status_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_fk_status']"))
            status_select.select_by_visible_text("Resuelto")
        except NoSuchElementException:
            status_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Estado')]")
            status_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='Resuelto']").click()
        
        # Seleccionar gravedad Alta
        try:
            severity_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_severity_id']"))
            severity_select.select_by_visible_text("Alto")
        except NoSuchElementException:
            severity_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Gravedad')]")
            severity_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='Alto']").click()
        
        # Verificar que solo se muestran tickets que cumplen ambos criterios
        def check_multiple_criteria(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[position() > 1]")
            if len(rows) == 0:
                return False
            
            for row in rows:
                status_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'status') or contains(text(), 'Resuelto')]")
                severity_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'severity') or contains(text(), 'Alto')]")
                
                if "Resuelto" not in status_cell.text or "Alto" not in severity_cell.text:
                    return False
            return True
        
        self.verify_results(
            expected_condition=check_multiple_criteria,
            error_message="Se muestran tickets que no cumplen ambos criterios (Resuelto + Alto)"
        )
    
    def test_CP18_filter_by_three_criteria(self):
        """CP18: Filtrar por tres criterios simultáneos"""
        self.navigate_to_tickets()
        self.clear_all_filters()
        
        # Seleccionar estado En progreso
        try:
            status_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_fk_status']"))
            status_select.select_by_visible_text("En progreso")
        except NoSuchElementException:
            status_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Estado')]")
            status_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='En progreso']").click()
        
        # Seleccionar gravedad Alta
        try:
            severity_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_severity_id']"))
            severity_select.select_by_visible_text("Alto")
        except NoSuchElementException:
            severity_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Gravedad')]")
            severity_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='Alto']").click()
        
        # Seleccionar usuario SuperAdmin
        try:
            user_select = Select(self.driver.find_element(By.XPATH, "//select[@name='search_fk_user_assign']"))
            user_select.select_by_visible_text("SuperAdmin")
        except NoSuchElementException:
            user_button = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Asignada a')]")
            user_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown-menu')]"))
            )
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[text()='SuperAdmin']").click()
        
        # Verificar que solo se muestran tickets que cumplen los tres criterios
        def check_three_criteria(driver):
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'liste')]/tbody/tr[position() > 1]")
            if len(rows) == 0:
                return False
            
            for row in rows:
                status_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'status') or contains(text(), 'En progreso')]")
                severity_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'severity') or contains(text(), 'Alto')]")
                user_cell = row.find_element(By.XPATH, ".//td[contains(@class, 'assigned') or contains(text(), 'SuperAdmin')]")
                
                if ("En progreso" not in status_cell.text or 
                    "Alto" not in severity_cell.text or 
                    "SuperAdmin" not in user_cell.text):
                    return False
            return True
        
        self.verify_results(
            expected_condition=check_three_criteria,
            error_message="Se muestran tickets que no cumplen los tres criterios (En progreso + Alto + SuperAdmin)"
        )
    
    def tearDown(self):
        """Cerrar el navegador después de cada prueba"""
        self.driver.quit()

if __name__ == "__main__":
    # Ejecutar las pruebas
    unittest.main()
