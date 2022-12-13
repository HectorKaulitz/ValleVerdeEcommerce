from Programacion.Funcionalidad.Encriptacion import Encriptacion



class getsetProducto:
    oben = Encriptacion()

    def __init__(self, idProducto, codigoBarras, nombreProducto, descripcionProducto, urlsImagenes,
                 mostrarEstrellas, puntuacion, precioOriginal, precioDescuento, costoEnvio, tieneEnvio,
                 tituloProductos, existencia, estaEnProductoFavorito, mostrarInteraccion):
        self.idProducto = idProducto
        self.codigoBarras = codigoBarras
        self.nombreProducto = nombreProducto
        self.descripcion = descripcionProducto
        self.urlsImagenes = urlsImagenes
        self.mostrarEstrellas = mostrarEstrellas
        self.puntuacion = puntuacion
        self.precioOriginal = self.obu.RedondeoDouble(str(precioOriginal))
        self.precioDescuento = self.obu.RedondeoDouble(str(precioDescuento))
        self.costoEnvio = self.obu.RedondeoDouble(str(costoEnvio))
        self.tieneEnvio = tieneEnvio
        self.tituloProductos = tituloProductos
        self.existencia = existencia
        self.estaEnProductoFavorito = estaEnProductoFavorito
        self.idProductoEncriptado = self.oben.Encrypt(str(idProducto))
        self.mostrarInteraccion = mostrarInteraccion
