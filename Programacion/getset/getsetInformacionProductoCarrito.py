class getsetInformacionProductoCarrito:
    idProductoCarrito = ""
    idProducto = ""
    idCarrito = ""
    cantidad = 0
    precioAgrego = 0
    precioPromocion = 0
    totalPrecioProducto = 0
    diferenciaPrecioAlQueAgrego = 0
    existencia = 0

    def __init__(self, idProductoCarrito, idProducto, idCarrito, cantidad, precioAgrego,
                 precioPromocion, totalPrecioProducto, diferenciaPrecioAlQueAgrego, existencia):
        self.idProductoCarrito = idProductoCarrito
        self.idProducto = idProducto
        self.idCarrito = idCarrito
        self.cantidad = cantidad
        self.precioAgrego = precioAgrego
        self.precioPromocion = precioPromocion
        self.totalPrecioProducto = totalPrecioProducto
        self.diferenciaPrecioAlQueAgrego = diferenciaPrecioAlQueAgrego
        self.existencia = existencia