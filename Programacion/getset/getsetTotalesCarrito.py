class getsetTotalesCarrito:
    fuentePequena = False
    totalSurtido = -1
    mostrarTotalSurtido = False

    def __init__(self, subtotal=0, envio=0, comision=0, descuento=0, total=0, enviarDomicilio=False, tipoPago=1):
        self.subtotal = float(subtotal)
        self.envio = float(envio)
        self.comision = float(comision)
        self.descuento = float(descuento)
        self.total = float(total)
        self.enviarDomicilio = enviarDomicilio
        self.tipoPago = tipoPago
        self.subtotalSinDescuento = float(subtotal + descuento)