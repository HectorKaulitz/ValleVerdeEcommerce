


class getsetObjetoPagoAprobado:
    def __init__(self, venta, idPagoMercadoPago,tipoPago,pagado,enProceso,rechazada,usuario,enviarADomicilio,urlCodigoBarras):
        from Programacion.Funcionalidad.Utileria import Utileria
        self.venta = venta
        self.idPagoMercadoPago = idPagoMercadoPago
        self.tipoPago = tipoPago
        self.pagado = pagado
        self.enProceso = enProceso
        self.rechazada = rechazada
        self.usuario = usuario
        self.enviarADomicilio = enviarADomicilio
        self.urlCodigoBarras = urlCodigoBarras