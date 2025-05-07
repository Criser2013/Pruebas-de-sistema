from playwright.sync_api import Page, expect
from datetime import datetime

class  CrearFacturaProvPage:
    """
    Clase que representa la página para crear facturas de proveedores en la aplicación.
    Proporciona métodos para interactuar con los elementos de la página, validar el
    guardado """

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina        
        self.__fecha = ""
        self.__usuario = ""
        self.__tipo_factura = ""
        self.__ref_factura = ""
        self.__pagina.goto(
            f"{url}/fourn/facture/card.php?leftmenu=suppliers_bills&action=create")
        
    def seleccionar_proveedor(self, usuario: str):
        """
        Selecciona el proveedor para la factura.
        Args:
            usuario (str): Nombre del proveedor a seleccionar.
        """
        assert (usuario is not None) and (len(usuario) > 0), "El nombre de usuario no puede estar vacío."

        self.__usuario = str(usuario)
        self.__pagina.locator("span[id='select2-socid-container']").click()
        self.__pagina.get_by_role("option", name=str(usuario)).click()
    
    def seleccionar_tipo_factura(self,tipo_factura: str, factura_abono:str|None = None):
        """
        Selecciona el tipo de factura a crear.
        Args:
            tipo_factura (str): Tipo de factura a seleccionar. Puede ser "estandar", "anticipo" o "abono".
            factura_abono (str): Nombre de la factura de abono a seleccionar. Solo utilizarlo si va a crear una factura de abono.
        """

        match (tipo_factura):
            case "estandar":
                self.__tipo_factura = "Factura estandar"
                self.__pagina.get_by_role("radio", name="Factura estandar").click()
            case "anticipo":
                self.__tipo_factura = "Factura de anticipo"
                self.__pagina.get_by_role("radio", name="Factura de anticipo").click()
            case "abono":
                self.__tipo_factura = "Nota de crédito"
                self.__pagina.get_by_role("radio", name="Nota de crédito para corregir factura").click()
                if factura_abono != "":
                    self.__pagina.locator("select[id='fac_avoir']").select_option(str(factura_abono))
            case _:
                raise ValueError("Tipo de factura no válido. Debe ser 'estandar', 'anticipo', 'rectificativa' o 'abono'.")

    def ingresar_fecha_factura(self, fecha: str = "", hoy: bool = False):
        """
        Ingresa la fecha de la factura en el campo correspondiente.
        Args:
            fecha (str): Fecha de la factura en formato DD/MM/AAAA.
            hoy (bool): Si es True, selecciona la fecha de hoy. Por defecto es False.
        """

        if hoy:
            self.__fecha = datetime.now().strftime("%d/%m/%Y")
            self.__pagina.locator("button[id='reButtonNow']").click()
        else:
            self.__fecha = str(fecha)
            self.__pagina.locator("input[id='re']").fill(str(fecha))
 
    def ingresar_ref_factura(self, ref_factura: str):
        """
        Ingresa la referencia de la factura en el campo correspondiente.
        Args:
            ref_factura (str): Referencia de la factura.
        """
        assert (ref_factura is not None) and (len(ref_factura) > 0), "La referencia de la factura no puede estar vacía."
        
        self.__ref_factura = str(ref_factura)
        self.__pagina.locator("input[name='ref_supplier']").fill(str(ref_factura))

    def guardar_factura(self):
        """
        Guarda la factura creada.
        """
        self.__pagina.get_by_role("button", name="Crear borrador").click()
    
    def verificar_guardado(self):
        """
        Verifica si la factura se ha guardado correctamente.
        """
        FECHA = self.__pagina.locator("span[class='valuedate']").all()[0]
        self.__pagina.wait_for_timeout(2000)
        # valindando el cliente
        expect(self.__pagina.locator("a[class='classfortooltip refurl valignmiddle']")).to_contain_text(self.__usuario)
        # validando la fecha
        expect(FECHA).to_have_text(self.__fecha)
        # validando el tipo de factura
        expect(self.__pagina.locator("span[class='badgeneutral']")).to_contain_text(self.__tipo_factura)
        # validando la referencia de la factura
        expect(self.__pagina.get_by_text(self.__ref_factura)).to_be_visible()

    def verificar_error(self, error: str):
        """
        Verifica si se ha producido un error al guardar la factura.
        """
        self.__pagina.wait_for_timeout(1000)
        expect(self.__pagina.locator("div[class='jnotify-message']")).to_contain_text(str(error))