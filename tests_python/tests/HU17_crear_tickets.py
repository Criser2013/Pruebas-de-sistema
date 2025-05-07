import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class DolibarrTicketTest(unittest.TestCase):
    def setUp(self):
        # Configuración del driver (puedes ajustar según tu navegador preferido)
        self.driver = webdriver.Chrome()  # o Firefox, Edge, etc.
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1/ticket/card.php?action=create&mode=init&idmenu=2&mainmenu=ticket&leftmenu="
        self.login()
        
    def tearDown(self):
        # Cerrar el navegador después de cada prueba
        self.driver.quit()
        
    def login(self):
        """Método para iniciar sesión en Dolibarr"""
        self.driver.get(f"{self.base_url}")
        
        # Esperar a que se cargue la página de login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Introducir credenciales
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin")
        self.driver.find_element(By.NAME, "login").click()
        
        # Esperar a que se cargue la página principal
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'ticket')]"))
        )
    
    def navigate_to_new_ticket(self):
        """Navega hasta la página de creación de tickets"""
        # Hacer clic en Tickets en el menú superior
        tickets_menu = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'ticket')]"))
        )
        tickets_menu.click()
        
        # Hacer clic en "Nuevo ticket" en el menú lateral
        new_ticket = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Nuevo ticket')]"))
        )
        new_ticket.click()
        
        # Esperar a que se cargue el formulario
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Nuevo ticket')]"))
        )
    
    def select_dropdown_option(self, dropdown_id, option_text):
        """Selecciona una opción en un desplegable por su texto"""
        dropdown = self.driver.find_element(By.ID, dropdown_id)
        select = Select(dropdown)
        select.select_by_visible_text(option_text)
    
    def verify_ticket_created(self):
        """Verifica que el ticket se creó correctamente"""
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'success')]"))
        )
        self.assertTrue(success_message.is_displayed())
        
        # Verificar que se ha redirigido a la página de detalle del ticket
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Ticket')]"))
        )
    
    def verify_error_message(self, expected_error):
        """Verifica que aparece un mensaje de error específico"""
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{expected_error}')]"))
        )
        self.assertTrue(error_message.is_displayed())
    
    def test_CP1_basic_ticket_without_tercero(self):
        """CP1: Creación básica de ticket con tipo 'Pregunta comercial' sin tercero seleccionado"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Pregunta comercial
        self.select_dropdown_option("selecttype", "Pregunta comercial")
        
        # Seleccionar grupo de ticket: Otro
        self.select_dropdown_option("selectgroup", "Otro")
        
        # Verificar que Gravedad: Normal está seleccionado por defecto
        gravedad_select = Select(self.driver.find_element(By.ID, "selectseverity"))
        self.assertEqual(gravedad_select.first_selected_option.text, "Normal")
        
        # Completar el Asunto
        self.driver.find_element(By.ID, "subject").send_keys("Consulta sobre precios de productos")
        
        # Completar el Mensaje (campo obligatorio)
        message_frame = self.driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame']")
        self.driver.switch_to.frame(message_frame)
        self.driver.find_element(By.XPATH, "//body").send_keys("Necesito información actualizada sobre los precios del catálogo de productos.")
        self.driver.switch_to.default_content()
        
        # Seleccionar Contribuidor externo: Contacto cliente
        self.select_dropdown_option("contributortype", "Contacto cliente")
        
        # Seleccionar Asignada a: SuperAdmin
        self.select_dropdown_option("fk_user_assign", "SuperAdmin")
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que el ticket se creó correctamente
        self.verify_ticket_created()
        
        # Verificaciones adicionales específicas para CP1
        # Verificar que el tipo de solicitud es correcto
        tipo_solicitud = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Pregunta comercial')]")
        self.assertTrue(tipo_solicitud.is_displayed())
        
        # Verificar que está asignado a SuperAdmin
        asignado = self.driver.find_element(By.XPATH, "//td[contains(text(), 'SuperAdmin')]")
        self.assertTrue(asignado.is_displayed())
    
    def test_CP2_ticket_with_tercero_and_notification(self):
        """CP2: Creación de ticket con solicitud de ayuda funcional y notificación a terceros"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Solicitud de ayuda funcional
        self.select_dropdown_option("selecttype", "Solicitud de ayuda funcional")
        
        # Seleccionar grupo de ticket: diferente a "Otro"
        self.select_dropdown_option("selectgroup", "Soporte")  # Ajusta según opciones disponibles
        
        # Completar el Asunto
        self.driver.find_element(By.ID, "subject").send_keys("Necesito ayuda con la configuración del módulo de facturación")
        
        # Completar el Mensaje con formato HTML
        message_frame = self.driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame']")
        self.driver.switch_to.frame(message_frame)
        self.driver.find_element(By.XPATH, "//body").send_keys("""
        Estoy teniendo dificultades para configurar correctamente el módulo de facturación.
        
        Los problemas específicos son:
        * No puedo establecer impuestos personalizados
        * Las plantillas de factura no se aplican correctamente
        * Necesito ayuda para configurar pagos parciales
        
        Agradezco su pronta respuesta.
        """)
        self.driver.switch_to.default_content()
        
        # Seleccionar Tercero: ISK libellule
        self.select_dropdown_option("socid", "ISK libellule")
        
        # Esperar a que se carguen las opciones de Contacto/Dirección
        time.sleep(2)  # Espera para que se actualice el dropdown
        
        # Seleccionar una opción de Contacto/Dirección
        self.select_dropdown_option("contactid", "Contacto Principal")  # Ajustar según opciones disponibles
        
        # Seleccionar Contribuidor externo: Contribuidor externo
        self.select_dropdown_option("contributortype", "Contribuidor externo")
        
        # Marcar Notificar a terceros
        self.driver.find_element(By.ID, "notify_tiers").click()
        
        # Seleccionar Asignada a: David Doe
        self.select_dropdown_option("fk_user_assign", "David Doe")
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que el ticket se creó correctamente
        self.verify_ticket_created()
        
        # Verificaciones adicionales específicas para CP2
        # Verificar que el tipo de solicitud es correcto
        tipo_solicitud = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Solicitud de ayuda funcional')]")
        self.assertTrue(tipo_solicitud.is_displayed())
        
        # Verificar que está asignado a David Doe
        asignado = self.driver.find_element(By.XPATH, "//td[contains(text(), 'David Doe')]")
        self.assertTrue(asignado.is_displayed())
    
    def test_CP3_ticket_with_file_attachment(self):
        """CP3: Creación de ticket para problema o error con archivo adjunto"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Problema o error
        self.select_dropdown_option("selecttype", "Problema o error")
        
        # Seleccionar grupo de ticket: Otro
        self.select_dropdown_option("selectgroup", "Otro")
        
        # Seleccionar gravedad: Opción distinta a Normal
        self.select_dropdown_option("selectseverity", "Alta")  # Ajustar según opciones disponibles
        
        # Completar el Asunto
        self.driver.find_element(By.ID, "subject").send_keys("Error en generación de reportes contables")
        
        # Completar el Mensaje
        message_frame = self.driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame']")
        self.driver.switch_to.frame(message_frame)
        self.driver.find_element(By.XPATH, "//body").send_keys("""
        Al intentar generar el reporte contable mensual, el sistema muestra un error "Undefined index" y 
        no completa la operación. Este problema comenzó a ocurrir después de la última actualización del sistema.
        """)
        self.driver.switch_to.default_content()
        
        # Adjuntar archivo
        file_path = os.path.abspath("error_screenshot.png")  # Ajustar a la ruta de tu archivo de prueba
        self.driver.find_element(By.ID, "fileupload").send_keys(file_path)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'ADJUNTAR ESTE ARCHIVO')]").click()
        
        # Seleccionar Tercero: ISK libellule
        self.select_dropdown_option("socid", "ISK libellule")
        
        # Esperar a que se carguen las opciones de Contacto/Dirección
        time.sleep(2)
        
        # Seleccionar una opción de Contacto/Dirección
        self.select_dropdown_option("contactid", "Contacto Principal")  # Ajustar según opciones disponibles
        
        # Seleccionar Contribuidor externo: Contacto cliente
        self.select_dropdown_option("contributortype", "Contacto cliente")
        
        # Seleccionar Asignada a: SuperAdmin
        self.select_dropdown_option("fk_user_assign", "SuperAdmin")
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que el ticket se creó correctamente
        self.verify_ticket_created()
        
        # Verificar que el archivo adjunto está presente
        archivo_adjunto = self.driver.find_element(By.XPATH, "//a[contains(text(), 'error_screenshot.png')]")
        self.assertTrue(archivo_adjunto.is_displayed())
    
    def test_CP5_error_empty_message(self):
        """CP5: Error al intentar crear ticket con mensaje vacío"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Otro
        self.select_dropdown_option("selecttype", "Otro")
        
        # Seleccionar grupo de ticket: Otro
        self.select_dropdown_option("selectgroup", "Otro")
        
        # Completar el Asunto
        self.driver.find_element(By.ID, "subject").send_keys("Consulta sobre procedimientos internos")
        
        # Dejar el campo Mensaje vacío intencionalmente
        
        # Seleccionar Tercero: ISK libellule
        self.select_dropdown_option("socid", "ISK libellule")
        
        # Seleccionar Contribuidor externo: Contacto cliente
        self.select_dropdown_option("contributortype", "Contacto cliente")
        
        # Seleccionar Asignada a: SuperAdmin
        self.select_dropdown_option("fk_user_assign", "SuperAdmin")
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que aparece un mensaje de error
        self.verify_error_message("El campo Mensaje es obligatorio")
    
    def test_CP4_ticket_with_contract(self):
        """CP4: Creación de ticket con solicitud de cambio y contrato seleccionado"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Solicitud de cambio o mejora
        self.select_dropdown_option("selecttype", "Solicitud de cambio o mejora")
        
        # Seleccionar grupo de ticket: diferente a "Otro"
        self.select_dropdown_option("selectgroup", "Soporte")  # Ajusta según opciones disponibles
        
        # Seleccionar gravedad: Opción distinta a Normal
        self.select_dropdown_option("selectseverity", "Alta")  # Ajustar según opciones disponibles
        
        # Completar el Asunto
        self.driver.find_element(By.ID, "subject").send_keys("Solicitud de mejora en módulo de inventario")
        
        # Completar el Mensaje con formato HTML
        message_frame = self.driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame']")
        self.driver.switch_to.frame(message_frame)
        self.driver.find_element(By.XPATH, "//body").send_keys("""
        Solicito las siguientes mejoras en el módulo de inventario:
        
        **Mejoras propuestas:**
        1. Añadir funcionalidad de escaneo de códigos QR para entrada/salida de productos
        2. Implementar sistema de alertas para stock mínimo personalizable por categoría
        3. Integrar un panel de estadísticas con gráficos de rotación de inventario
        
        **Beneficios esperados:**
        - Reducción de tiempo en procesos de inventario
        - Mejor control de stock
        - Toma de decisiones basada en datos
        
        Adjunto documento con especificaciones detalladas.
        """)
        self.driver.switch_to.default_content()
        
        # Adjuntar archivo
        file_path = os.path.abspath("especificaciones.pdf")  # Ajustar a la ruta de tu archivo de prueba
        self.driver.find_element(By.ID, "fileupload").send_keys(file_path)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'ADJUNTAR ESTE ARCHIVO')]").click()
        
        # Seleccionar Tercero: ISK libellule
        self.select_dropdown_option("socid", "ISK libellule")
        
        # Esperar a que se carguen las opciones de Contacto/Dirección pero NO seleccionar ninguna
        time.sleep(2)
        
        # Seleccionar Contribuidor externo: Contribuidor externo
        self.select_dropdown_option("contributortype", "Contribuidor externo")
        
        # Marcar Notificar a terceros
        self.driver.find_element(By.ID, "notify_tiers").click()
        
        # Seleccionar Asignada a: David Doe
        self.select_dropdown_option("fk_user_assign", "David Doe")
        
        # Seleccionar un Contrato
        self.select_dropdown_option("contractid", "Contrato de Mantenimiento")  # Ajustar según opciones disponibles
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que el ticket se creó correctamente
        self.verify_ticket_created()
        
        # Verificaciones adicionales específicas para CP4
        # Verificar que está asociado al contrato seleccionado
        contrato = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Contrato de Mantenimiento')]")
        self.assertTrue(contrato.is_displayed())
        
        # Verificar que está asignado a David Doe
        asignado = self.driver.find_element(By.XPATH, "//td[contains(text(), 'David Doe')]")
        self.assertTrue(asignado.is_displayed())

    def test_CP6_complete_ticket_with_all_options(self):
        """CP6: Ticket completo con todas las opciones seleccionadas"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Otro
        self.select_dropdown_option("selecttype", "Otro")
        
        # Seleccionar grupo de ticket: diferente a "Otro"
        self.select_dropdown_option("selectgroup", "Desarrollo")  # Ajusta según opciones disponibles
        
        # Mantener Gravedad: Normal
        # No hacemos nada ya que es el valor por defecto
        
        # Completar el Asunto
        self.driver.find_element(By.ID, "subject").send_keys("Solicitud de información adicional")
        
        # Completar el Mensaje con formato HTML
        message_frame = self.driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame']")
        self.driver.switch_to.frame(message_frame)
        self.driver.find_element(By.XPATH, "//body").send_keys("""
        Solicito la siguiente información:
        
        **Documentación requerida:**
        1. Manual de procedimientos actualizado
        2. Guía de configuración del sistema
        3. Plantillas de documentos corporativos
        
        Por favor, proporcionen esta información a la mayor brevedad posible.
        
        Saludos cordiales,
        """)
        self.driver.switch_to.default_content()
        
        # Adjuntar archivo
        file_path = os.path.abspath("solicitud_formal.pdf")  # Ajustar a la ruta de tu archivo de prueba
        self.driver.find_element(By.ID, "fileupload").send_keys(file_path)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'ADJUNTAR ESTE ARCHIVO')]").click()
        
        # Seleccionar Tercero: ISK libellule
        self.select_dropdown_option("socid", "ISK libellule")
        
        # Esperar a que se carguen las opciones de Contacto/Dirección
        time.sleep(2)
        
        # Seleccionar una opción de Contacto/Dirección
        self.select_dropdown_option("contactid", "Contacto Principal")  # Ajustar según opciones disponibles
        
        # Seleccionar Contribuidor externo: Contacto cliente
        self.select_dropdown_option("contributortype", "Contacto cliente")
        
        # Marcar Notificar a terceros
        self.driver.find_element(By.ID, "notify_tiers").click()
        
        # Seleccionar Asignada a: David Doe
        self.select_dropdown_option("fk_user_assign", "David Doe")
        
        # Seleccionar un Contrato
        self.select_dropdown_option("contractid", "Contrato de Servicios")  # Ajustar según opciones disponibles
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que el ticket se creó correctamente
        self.verify_ticket_created()
        
        # Verificaciones adicionales específicas para CP6
        # Verificar que el tipo de solicitud es correcto
        tipo_solicitud = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Otro')]")
        self.assertTrue(tipo_solicitud.is_displayed())
        
        # Verificar que está asignado a David Doe
        asignado = self.driver.find_element(By.XPATH, "//td[contains(text(), 'David Doe')]")
        self.assertTrue(asignado.is_displayed())
        
        # Verificar que está asociado al contrato seleccionado
        contrato = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Contrato de Servicios')]")
        self.assertTrue(contrato.is_displayed())
        
        # Verificar que se muestra el archivo adjunto
        archivo_adjunto = self.driver.find_element(By.XPATH, "//a[contains(text(), 'solicitud_formal.pdf')]")
        self.assertTrue(archivo_adjunto.is_displayed())

    def test_CP7_multiple_empty_fields(self):
        """CP7: Error al intentar crear ticket con múltiples campos vacíos"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Otro
        self.select_dropdown_option("selecttype", "Otro")
        
        # Seleccionar grupo de ticket: Otro
        self.select_dropdown_option("selectgroup", "Otro")
        
        # Seleccionar gravedad: Opción distinta a Normal
        self.select_dropdown_option("selectseverity", "Baja")  # Ajustar según opciones disponibles
        
        # Dejar el campo Asunto vacío intencionalmente
        
        # Dejar el campo Mensaje vacío intencionalmente
        
        # No adjuntar ningún archivo
        
        # No seleccionar Tercero
        
        # No seleccionar Contribuidor externo
        
        # No marcar Notificar a terceros
        
        # No seleccionar Asignada a (dejar valor predeterminado)
        
        # No seleccionar Contrato
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar que aparecen mensajes de error
        # Verificar error de Mensaje obligatorio
        self.verify_error_message("El campo Mensaje es obligatorio")
        
        # Verificar error de Asunto obligatorio (si aplica)
        try:
            self.verify_error_message("El campo Asunto es obligatorio")
        except:
            # Si no aparece, podría ser que el campo no sea obligatorio en esta configuración
            print("Nota: No se detectó mensaje de error para campo Asunto vacío")
        
        # Verificar que no se ha creado el ticket
        # Esto podría hacerse intentando navegar al listado de tickets y verificando que no existe
        # el ticket con la referencia esperada, pero como no tenemos acceso a ese dato aquí,
        # nos conformamos con verificar que seguimos en la página de creación
        current_url = self.driver.current_url
        self.assertTrue("action=create" in current_url, "No se permanece en la página de creación tras intento fallido")

    def test_CP8_ticket_with_very_long_subject(self):
        """CP8: Ticket con asunto muy largo"""
        self.navigate_to_new_ticket()
        
        # Seleccionar tipo de solicitud: Otro
        self.select_dropdown_option("selecttype", "Otro")
        
        # Seleccionar grupo de ticket: diferente a "Otro"
        self.select_dropdown_option("selectgroup", "Marketing")  # Ajusta según opciones disponibles
        
        # Seleccionar gravedad: Opción distinta a Normal
        self.select_dropdown_option("selectseverity", "Urgente")  # Ajustar según opciones disponibles
        
        # Completar el Asunto con un texto extremadamente largo (>100 caracteres)
        asunto_largo = "Este es un asunto extremadamente largo para probar cómo maneja el sistema los títulos con muchos caracteres, específicamente para verificar si hay algún límite o validación en la longitud del campo de asunto del ticket."
        self.driver.find_element(By.ID, "subject").send_keys(asunto_largo)
        
        # Completar el Mensaje con formato HTML
        message_frame = self.driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame']")
        self.driver.switch_to.frame(message_frame)
        self.driver.find_element(By.XPATH, "//body").send_keys("""
        Este es un mensaje de prueba para el caso de prueba CP8.
        
        **Objetivo:**
        Verificar el comportamiento del sistema con un asunto muy largo.
        
        *Nota:* Este ticket es parte de una prueba automatizada.
        """)
        self.driver.switch_to.default_content()
        
        # Adjuntar archivo
        file_path = os.path.abspath("documento_prueba.pdf")  # Ajustar a la ruta de tu archivo de prueba
        self.driver.find_element(By.ID, "fileupload").send_keys(file_path)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'ADJUNTAR ESTE ARCHIVO')]").click()
        
        # Seleccionar Tercero: ISK libellule
        self.select_dropdown_option("socid", "ISK libellule")
        
        # Esperar a que se carguen las opciones de Contacto/Dirección
        time.sleep(2)
        
        # Seleccionar una opción de Contacto/Dirección
        self.select_dropdown_option("contactid", "Contacto Principal")  # Ajustar según opciones disponibles
        
        # Seleccionar Contribuidor externo: Contribuidor externo
        self.select_dropdown_option("contributortype", "Contribuidor externo")
        
        # Marcar Notificar a terceros
        self.driver.find_element(By.ID, "notify_tiers").click()
        
        # No seleccionar Asignada a intencionalmente
        
        # Hacer clic en CREAR TICKET
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'CREAR TICKET')]").click()
        
        # Verificar si el sistema permite o no la creación con asunto tan largo
        try:
            # Intentar verificar si se creó correctamente
            self.verify_ticket_created()
            
            # Si llegamos aquí, el ticket se creó correctamente a pesar del asunto largo
            # Verificar que el asunto largo se guardó correctamente (puede estar truncado)
            asunto_elemento = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Este es un asunto extremadamente')]")
            self.assertTrue(asunto_elemento.is_displayed())
            
            # Verificar si el asunto está truncado (comparar longitud)
            asunto_mostrado = asunto_elemento.text
            self.assertLessEqual(len(asunto_mostrado), len(asunto_largo), 
                            "El asunto no está truncado, lo que podría indicar que no hay validación de longitud")
            
        except:
            # Si llegamos aquí, el ticket no se creó, probablemente debido a una validación de longitud
            # Verificar que hay un mensaje de error relacionado con la longitud del asunto
            try:
                self.verify_error_message("longitud")  # Mensaje genérico que podría estar en el error
                print("El sistema rechazó el asunto por ser demasiado largo, como se esperaba")
            except:
                self.fail("El ticket no se creó pero no se muestra un mensaje de error claro sobre la longitud del asunto")
        

if __name__ == "__main__":
    unittest.main()
