from Programacion.Funcionalidad.Encriptacion import Encriptacion



class getsetProducto:

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
        self.precioOriginal = precioOriginal
        self.precioDescuento = precioDescuento
        self.costoEnvio = costoEnvio
        self.tieneEnvio = tieneEnvio
        self.tituloProductos = tituloProductos
        self.existencia = existencia
        self.estaEnProductoFavorito = estaEnProductoFavorito
        self.idProductoEncriptado =idProducto
        self.mostrarInteraccion = mostrarInteraccion
