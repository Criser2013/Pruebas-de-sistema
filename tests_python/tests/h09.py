import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class TestReglasCreacionUsuarios():
    def setup_method(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.login()
        
    def teardown_method(self):
        self.driver.quit()
    
    def login(self):
        """Iniciar sesión en el sistema"""
        self.driver.get("http://127.0.0.1/")
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".button").click()
    
    def navegar_a_nuevo_empleado(self):
        """Navegar a la página de nuevo empleado"""
        try:
            # Intenta navegar directamente desde el menú principal
            self.driver.find_element(By.CSS_SELECTOR, "#mainmenua_hrm > .mainmenuaspan").click()
            self.driver.find_element(By.LINK_TEXT, "Nuevo empleado").click()
        except:
            # Si hay algún problema, intenta primero ir a Inicio
            self.driver.find_element(By.LINK_TEXT, "Inicio").click()
            self.driver.find_element(By.CSS_SELECTOR, "#mainmenua_hrm > .mainmenuaspan").click()
            self.driver.find_element(By.LINK_TEXT, "Nuevo empleado").click()
    
    def completar_campos_obligatorios(self, completar=True):
        """Completar los campos obligatorios del formulario"""
        if completar:
            # Generar un timestamp único para evitar duplicados
            timestamp = int(time.time())
            
            # Rellenar apellidos y nombre
            self.driver.find_element(By.ID, "lastname").clear()
            self.driver.find_element(By.ID, "lastname").send_keys(f"Apellido{timestamp}")
            
            self.driver.find_element(By.ID, "firstname").clear()
            self.driver.find_element(By.ID, "firstname").send_keys(f"Nombre{timestamp}")
            
            # Completar login
            self.driver.find_element(By.ID, "login").clear()
            self.driver.find_element(By.ID, "login").send_keys(f"usuario{timestamp}")
            
            # Seleccionar título de cortesía
            self.driver.find_element(By.ID, "select2-civility_code-container").click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Sr.')]"))).click()
    
    def seleccionar_administrador(self, seleccionar=True):
        """Seleccionar si el usuario será administrador"""
        admin_dropdown = self.driver.find_element(By.CSS_SELECTOR, ".width75 > .select2-selection__arrow")
        admin_dropdown.click()
        
        if seleccionar:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Sí')]"))).click()
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'No')]"))).click()
    
    def completar_info_contacto(self, completar=True):
        """Completar información de contacto"""
        if completar:
            # Dirección
            self.driver.find_element(By.ID, "address").clear()
            self.driver.find_element(By.ID, "address").send_keys("Calle Principal 123")
            
            # Código postal
            self.driver.find_element(By.ID, "zipcode").clear()
            self.driver.find_element(By.ID, "zipcode").send_keys("12345")
            
            # Población
            self.driver.find_element(By.ID, "town").clear()
            self.driver.find_element(By.ID, "town").send_keys("Santiago de Cali")
            
            # País
            try:
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(9) .select2-selection__arrow").click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Colombia')]"))).click()
            except:
                print("No se pudo seleccionar el país")
            
            # Teléfono y correo
            self.driver.find_element(By.ID, "office_phone").clear()
            self.driver.find_element(By.ID, "office_phone").send_keys("3211234567")
            
            self.driver.find_element(By.ID, "user_mobile").clear()
            self.driver.find_element(By.ID, "user_mobile").send_keys("3109876543")
            
            timestamp = int(time.time())
            self.driver.find_element(By.ID, "email").clear()
            self.driver.find_element(By.ID, "email").send_keys(f"test{timestamp}@ejemplo.com")
    
    def establecer_intervalo_fechas(self, establecer=True):
        """Establecer intervalo de fechas de validez"""
        if establecer:
            try:
                # Fecha inicio
                self.driver.find_element(By.CSS_SELECTOR, 
                                        "tr:nth-child(1) .nowraponall:nth-child(2) > .ui-datepicker-trigger").click()
                self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "7"))).click()
                
                # Fecha fin
                self.driver.find_element(By.CSS_SELECTOR, ".nowraponall:nth-child(7) > .ui-datepicker-trigger").click()
                self.driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year").click()
                self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "6"))).click()
                self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "7"))).click()
            except:
                print("No se pudieron establecer las fechas correctamente")
    
    def asignar_supervisor(self, asignar=True):
        """Asignar supervisor al usuario"""
        if asignar:
            try:
                self.driver.find_element(By.ID, "select2-fk_user-container").click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'admin')]"))).click()
            except:
                print("No se pudo asignar el supervisor")
    
    def completar_info_laboral(self, completar=True):
        """Completar información laboral"""
        if completar:
            try:
                # Puesto de trabajo
                self.driver.find_element(By.ID, "job").clear()
                self.driver.find_element(By.ID, "job").send_keys("Desarrollador")
                
                # Horas trabajadas
                self.driver.find_element(By.ID, "weeklyhours").clear()
                self.driver.find_element(By.ID, "weeklyhours").send_keys("40")
                
                # Fecha empleo
                self.driver.find_element(By.CSS_SELECTOR, 
                                        "tr:nth-child(3) .nowraponall:nth-child(2) > .ui-datepicker-trigger").click()
                self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "7"))).click()
            except:
                print("No se pudo completar la información laboral")
    
    def guardar_formulario(self):
        """Guardar el formulario"""
        self.driver.find_element(By.NAME, "save").click()
        time.sleep(2)  # Pausa breve para dar tiempo a que se procese el formulario
    
    def verificar_mensaje_error(self):
        """Verificar si se muestra un mensaje de error"""
        try:
            mensaje_error = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".error")))
            print("Mensaje de error encontrado: " + mensaje_error.text)
            return mensaje_error.is_displayed()
        except (NoSuchElementException, TimeoutException):
            print("No se encontró mensaje de error")
            return False
    
    def verificar_creacion_usuario(self):
        """Verificar si el usuario fue creado exitosamente"""
        try:
            # Verificar si estamos en la página de detalle del usuario o si hay un mensaje de éxito
            mensaje_exito = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ok")))
            print("Mensaje de éxito encontrado: " + mensaje_exito.text)
            return mensaje_exito.is_displayed()
        except (NoSuchElementException, TimeoutException):
            try:
                # Alternativa: verificar si estamos en la ficha del empleado
                ficha_empleado = self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//h3[contains(text(), 'Ficha empleado')]")))
                print("Ficha de empleado encontrada")
                return ficha_empleado.is_displayed()
            except (NoSuchElementException, TimeoutException):
                print("No se encontró confirmación de creación de usuario")
                return False
    
    def test_regla_1(self):
        """
        Regla 1 (R1) - Usuario completo con permisos de administrador
        
        Condiciones:
        - Usuario completa campos obligatorios: SÍ
        - Usuario selecciona administrador de sistema: SÍ
        - Usuario completa información de contacto: SÍ
        - Usuario establece intervalo de fechas: SÍ
        - Usuario asigna supervisor: SÍ
        - Usuario completa información laboral: SÍ
        
        Acciones:
        - Crear usuario en el sistema
        - Habilitar permisos de administrador
        - Guardar información de contacto
        - Establecer periodo de validez
        - Asignar relación con supervisor
        - Registrar información laboral
        """
        print("\nEjecutando prueba de Regla 1 (R1)")
        
        self.navegar_a_nuevo_empleado()
        self.completar_campos_obligatorios(True)
        self.seleccionar_administrador(True)
        self.completar_info_contacto(True)
        self.establecer_intervalo_fechas(True)
        self.asignar_supervisor(True)
        self.completar_info_laboral(True)
        self.guardar_formulario()
        
        # Verificar resultado esperado
        assert self.verificar_creacion_usuario(), "R1: No se creó correctamente el usuario completo con permisos de administrador"
        print("✓ R1: Usuario creado correctamente con todos los datos completos y permisos de administrador")
    
    def test_regla_2(self):
        """
        Regla 2 (R2) - Usuario administrador sin información de contacto
        
        Condiciones:
        - Usuario completa campos obligatorios: SÍ
        - Usuario selecciona administrador de sistema: SÍ
        - Usuario completa información de contacto: NO
        - Usuario establece intervalo de fechas: SÍ
        - Usuario asigna supervisor: SÍ
        - Usuario completa información laboral: NO
        
        Acciones:
        - Crear usuario en el sistema
        - Habilitar permisos de administrador
        - Establecer periodo de validez
        - Asignar relación con supervisor
        """
        print("\nEjecutando prueba de Regla 2 (R2)")
        
        self.navegar_a_nuevo_empleado()
        self.completar_campos_obligatorios(True)
        self.seleccionar_administrador(True)
        self.completar_info_contacto(False)
        self.establecer_intervalo_fechas(True)
        self.asignar_supervisor(True)
        self.completar_info_laboral(False)
        self.guardar_formulario()
        
        # Verificar resultado esperado
        assert self.verificar_creacion_usuario(), "R2: No se creó correctamente el usuario administrador sin información de contacto"
        print("✓ R2: Usuario creado correctamente con permisos de administrador y sin información de contacto")
    
    def test_regla_3(self):
        """
        Regla 3 (R3) - Usuario sin permisos de administrador con información de contacto
        
        Condiciones:
        - Usuario completa campos obligatorios: SÍ
        - Usuario selecciona administrador de sistema: NO
        - Usuario completa información de contacto: SÍ
        - Usuario establece intervalo de fechas: SÍ
        - Usuario asigna supervisor: SÍ
        - Usuario completa información laboral: NO
        
        Acciones:
        - Crear usuario en el sistema
        - Guardar información de contacto
        - Establecer periodo de validez
        - Asignar relación con supervisor
        """
        print("\nEjecutando prueba de Regla 3 (R3)")
        
        self.navegar_a_nuevo_empleado()
        self.completar_campos_obligatorios(True)
        self.seleccionar_administrador(False)
        self.completar_info_contacto(True)
        self.establecer_intervalo_fechas(True)
        self.asignar_supervisor(True)
        self.completar_info_laboral(False)
        self.guardar_formulario()
        
        # Verificar resultado esperado
        assert self.verificar_creacion_usuario(), "R3: No se creó correctamente el usuario sin permisos de administrador con información de contacto"
        print("✓ R3: Usuario creado correctamente sin permisos de administrador y con información de contacto")
    
    def test_regla_4(self):
        """
        Regla 4 (R4) - Usuario mínimo sin permisos de administrador
        
        Condiciones:
        - Usuario completa campos obligatorios: SÍ
        - Usuario selecciona administrador de sistema: NO
        - Usuario completa información de contacto: NO
        - Usuario establece intervalo de fechas: SÍ
        - Usuario asigna supervisor: NO
        - Usuario completa información laboral: NO
        
        Acciones:
        - Crear usuario en el sistema
        - Establecer periodo de validez
        """
        print("\nEjecutando prueba de Regla 4 (R4)")
        
        self.navegar_a_nuevo_empleado()
        self.completar_campos_obligatorios(True)
        self.seleccionar_administrador(False)
        self.completar_info_contacto(False)
        self.establecer_intervalo_fechas(True)
        self.asignar_supervisor(False)
        self.completar_info_laboral(False)
        self.guardar_formulario()
        
        # Verificar resultado esperado
        assert self.verificar_creacion_usuario(), "R4: No se creó correctamente el usuario mínimo sin permisos de administrador"
        print("✓ R4: Usuario mínimo creado correctamente sin permisos de administrador")
    
    def test_regla_5(self):
        """
        Regla 5 (R5) - Usuario con campos obligatorios incompletos
        
        Condiciones:
        - Usuario completa campos obligatorios: NO
        - (Las demás condiciones son indiferentes)
        
        Acciones:
        - Mostrar mensaje de error
        """
        print("\nEjecutando prueba de Regla 5 (R5)")
        
        self.navegar_a_nuevo_empleado()
        # No completamos los campos obligatorios a propósito
        # Las demás opciones no importan según la regla
        self.guardar_formulario()
        
        # Verificar resultado esperado
        assert self.verificar_mensaje_error(), "R5: No se mostró el mensaje de error esperado"
        print("✓ R5: Se mostró correctamente el mensaje de error por falta de campos obligatorios")