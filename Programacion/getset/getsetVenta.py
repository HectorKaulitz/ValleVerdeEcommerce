


class getsetVenta:
    def __init__(self, idVenta, idUsuario, fechaVenta, pagada, idPreferenciaMercadoPago, enviarADomicilio,
                 subtotal, costoEnvio, total, estatusVenta, idTipoPago, idVentaEncriptada, idPagoMercadoPago,
                 idCargoOpenpay):
        from Programacion.Funcionalidad.Utileria import Utileria
        self.idVenta = idVenta
        self.idUsuario = idUsuario
        self.fechaVenta = fechaVenta
        self.pagada = pagada
        self.idPreferenciaMercadoPago = idPreferenciaMercadoPago
        self.enviarADomicilio = enviarADomicilio
        self.subtotal = Utileria().RedondeoDouble(subtotal)
        self.costoEnvio = Utileria().RedondeoDouble(costoEnvio)
        self.total = Utileria().RedondeoDouble(total)
        self.estatusVenta = estatusVenta
        self.idTipoPago = idTipoPago
        self.idVentaEncriptada = idVentaEncriptada
        self.idPagoMercadoPago = idPagoMercadoPago
        self.idCargoOpenpay = idCargoOpenpay