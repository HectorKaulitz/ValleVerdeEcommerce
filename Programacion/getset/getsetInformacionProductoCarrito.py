class getsetInformacionProductoCarrito:
    # idProductoCarrito = ""
    # idProducto = ""
    # idCarrito = ""
    # cantidad = 0
    # precioAgrego = 0
    # precioPromocion = 0
    # totalPrecioProducto = 0
    # diferenciaPrecioAlQueAgrego = 0
    # existencia = 0

    def __init__(self, idProductoCarrito, idProducto, idCarrito, cantidad, precioAgrego,
                 precioPromocion, totalPrecioProducto, diferenciaPrecioAlQueAgrego, existencia):
        self.idProductoCarrito = idProductoCarrito
        self.idProducto = idProducto
        self.idCarrito = idCarrito
        self.cantidad = float(cantidad)
        self.precioAgrego = float(precioAgrego)
        self.precioPromocion = float(precioPromocion)
        self.totalPrecioProducto = float(totalPrecioProducto)
        self.diferenciaPrecioAlQueAgrego = float(diferenciaPrecioAlQueAgrego)
        self.existencia = existencia