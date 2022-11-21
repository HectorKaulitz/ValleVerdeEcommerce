class getsetObjetoCarritoFlotante:
    datosUsuario = None
    productosCarrito = []
    totalesCarrito = None

    def __init__(self, productosCarrito, totalesCarrito, datosUsuario):
        self.productosCarrito = productosCarrito
        self.totalesCarrito = totalesCarrito
        self.datosUsuario = datosUsuario