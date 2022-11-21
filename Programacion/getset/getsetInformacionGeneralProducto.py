class getsetInformacionGeneralProducto:
    NumeroTotalProductos = 0
    TipoPagina = 0
    productosPag = 0
    NumeroCuadrosPagina = 0

    def __init__(self, numeroProductosTotal, tipoPagina, productosPag, NumeroCuadrosPagina):
        self.NumeroTotalProductos = numeroProductosTotal
        self.TipoPagina = tipoPagina
        self.productosPag = productosPag
        self.NumeroCuadrosPagina = NumeroCuadrosPagina