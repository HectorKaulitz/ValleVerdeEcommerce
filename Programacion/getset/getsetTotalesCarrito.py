class getsetTotalesCarrito:
    fuentePequena = False
    totalSurtido = -1
    mostrarTotalSurtido = False

    def __init__(self, subtotal=0, envio=0, comision=0, descuento=0, total=0, enviarDomicilio=False, tipoPago=1):
        self.subtotal = subtotal
        self.envio = envio
        self.comision = comision
        self.descuento = descuento
        self.total = total
        self.enviarDomicilio = enviarDomicilio
        self.tipoPago = tipoPago
        self.subtotalSinDescuento = subtotal + descuento