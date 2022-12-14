class getsetProductoCarrito:


    def __init__(self, indice, idUsuarioRegistrado, idProducto, nombre, descripcion, bloqueado,
                idLinea, idSubLinea, idMarca, precioOriginal, precioPromocion, idCarrito,
                idProducto_Carrito, cantidad, precioAgrego, importeProducto, urlsImagenes,
                existencia, codigoBarras, descuento, descuentoTotal):

        from Programacion.Funcionalidad.Utileria import Utileria
        obu = Utileria()

        self.indice = indice;
        self.idUsuarioRegistrado = idUsuarioRegistrado;
        self.idProducto = idProducto;
        self.nombre = nombre;
        self.descripcion = descripcion;
        self.bloqueado = bloqueado;
        self.idLinea = idLinea;
        self.idSubLinea = idSubLinea;
        self.idMarca = idMarca;
        self.precioOriginal = obu.RedondeoDouble(str(precioOriginal));
        self.precioPromocion = obu.RedondeoDouble(str(precioPromocion));
        self.idCarrito = idCarrito;
        self.idProducto_Carrito = idProducto_Carrito;
        self.cantidad = cantidad;
        self.precioAgrego = obu.RedondeoDouble(str(precioAgrego));
        self.importeProducto = obu.RedondeoDouble(str(importeProducto));
        self.importeOriginalProducto = obu.RedondeoDouble(str(precioOriginal * cantidad));
        self.urlsImagenes = urlsImagenes;
        self.existencia = existencia;
        self.codigoBarras = codigoBarras;
        self.DiferenciaConPrecioActual = round(precioPromocion - precioAgrego, 2);
        self.descuento = descuento;
        self.descuentoTotal = descuentoTotal;