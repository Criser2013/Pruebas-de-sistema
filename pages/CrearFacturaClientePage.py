from playwright.sync_api import Page, expect
from datetime import datetime

class  CrearFacturaClientePage:
    """
    Clase que representa la página para crear facturas de clientes en la aplicación.
    Proporciona métodos para interactuar con los elementos de la página, validar el
    guardado """

    def __init__(self, pagina: Page, url: str):
        self.__pagina = pagina        
        self.__pagina.goto(
            f"{url}/compta/facture/card.php?action=create&leftmenu=")
        
    def seleccionar_cliente(self, usuario: str):
        """
        Selecciona el cliente para la factura.
        Args:
            usuario (str): Nombre del cliente a seleccionar.
        """
        assert (usuario is not None) and (len(usuario) > 0), "El nombre de usuario no puede estar vacío."

        self.__usuario = str(usuario)
        self.__pagina.locator("span[id='select2-socid-container']").click()
        self.__pagina.get_by_role("option", name=str(usuario)).click()
    
    def seleccionar_tipo_factura(self,tipo_factura: str, factura_rectificativa: str|None = None, factura_abono:str|None = None):
        """
        Selecciona el tipo de factura a crear.
        Args:
            factura_rectificativa (str): Nombre de la factura rectificativa a seleccionar. Solo utilizarlo si va a crear una factura rectificativa.
            factura_abono (str): Nombre de la factura de abono a seleccionar. Solo utilizarlo si va a crear una factura de abono.
        """

        #print(factura_rectificativa, factura_abono)

        #assert (((factura_rectificativa is not None) and (len(factura_rectificativa)>0))) and ((factura_abono is not None) and (len(factura_rectificativa)>0)), "Debe seleccionar un solo tipo de factura."
        """        assert (tipo_factura is not None) and (len(tipo_factura) > 0), "El tipo de factura no puede estar vacío."
        assert (tipo_factura == "rectificativa") and ((factura_rectificativa is None) or (len(factura_rectificativa) > 0)), "La factura rectificativa no puede estar vacía."
        assert (tipo_factura == "abono") and ((factura_abono is None) or (len(factura_abono) > 0)), "La factura de abono no puede estar vacía."""

        match (tipo_factura):
            case "estandar":
                self.__tipo_factura = "Estándar"
                self.__pagina.get_by_role("radio", name="Factura estandar").click()
            case "anticipo":
                self.__tipo_factura = "Pago inicial"
                self.__pagina.get_by_role("radio", name="Factura de anticipo").click()
            case "rectificativa":
                self.__tipo_factura = "Reemplazo"
                self.__pagina.get_by_role("radio", name="Factura de reemplazo para la factura.").click()
                if factura_rectificativa != "":
                    self.__pagina.locator("span[id='select2-fac_replacement-container']").click()
                    self.__pagina.get_by_role("option", name=str(factura_rectificativa)).click()
            case "abono":
                self.__tipo_factura = "Nota de crédito"
                self.__pagina.get_by_role("radio", name="Nota de crédito para corregir factura").click()
                if factura_abono != "":
                    self.__pagina.locator("span[role='combobox'][class='select2-selection select2-selection--single flat valignmiddle']").click()
                    self.__pagina.get_by_role("option", name=str(factura_abono)).click()
            case _:
                raise ValueError("Tipo de factura no válido. Debe ser 'estandar', 'anticipo', 'rectificativa' o 'abono'.")

    def ingresar_fecha_factura(self, fecha: str = "", hoy: bool = False):
        """
        Ingresa la fecha de la factura en el campo correspondiente.
        Args:
            fecha (str): Fecha de la factura en formato DD/MM/AAAA.
            hoy (bool): Si es True, selecciona la fecha de hoy. Por defecto es False.
        """
        #assert (not hoy) and (fecha is not None) and (len(fecha) > 0), "La fecha no puede estar vacía."

        if hoy:
            self.__fecha = datetime.now().strftime("%d/%m/%Y")
            self.__pagina.get_by_role("button", name="Ahora").click()
        else:
            self.__fecha = str(fecha)
            print(fecha)
            self.__pagina.locator("input[id='re']").fill(str(fecha))

    def seleccionar_condicion_pago(self, condicion_pago: str):
        """
        Selecciona la condición de pago de la factura.
        Args:
            condicion_pago (str): Condición de pago a seleccionar.
        """
        assert (condicion_pago is not None) and (len(condicion_pago) > 0), "La condición de pago no puede estar vacía."

        self.__cond_pago = str(condicion_pago)
        self.__pagina.locator("span[id='select2-cond_reglement_id-container']").click()
        self.__pagina.get_by_role("option", name=str(condicion_pago)).click()

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
        # validando la condicion de pago
        expect(self.__pagina.get_by_text(self.__cond_pago)).to_be_visible()

    def verificar_error(self, error: str):
        """
        Verifica si se ha producido un error al guardar la factura.
        """
        self.__pagina.wait_for_timeout(1000)
        expect(self.__pagina.locator("div[class='jnotify-message']")).to_contain_text(str(error))