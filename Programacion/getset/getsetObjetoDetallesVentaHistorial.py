class getsetObjetoDetallesVentaHistorial:
    productosVenta = []
    totalesVenta = None
    estatusVenta = 0

    def __init__(self, productosVenta,  totalesVenta, estatusVenta):
        self.productosVenta = productosVenta
        self.totalesVenta = totalesVenta
        self.estatusVenta = estatusVenta