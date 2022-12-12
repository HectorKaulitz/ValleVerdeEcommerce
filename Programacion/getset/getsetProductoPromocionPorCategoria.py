from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.Utileria import Utileria


class getsetProductoPromocionPorCategoria:
    obu = Utileria()
    oben = Encriptacion()

    def __init__(self, idProducto, codigoBarras, nombreProducto, descripcionProducto, idDependiendoCategoria,nombreDependiendoCategoria,IDPromocionTablaVarianteDeCategoria,
                 IDPromocion,NombrePromocion,Descuento,Impresa,IDHorarioPromocion,FechaInicio,FechaFin,LimitePorCliente,imagenes,precio,PrecioPromocion,
                 puntuacion,tieneEnvio,costoEnvio,estaEnProductoFavorito,mostrarInteraccion):
        self.idProducto = idProducto
        self.codigoBarras = codigoBarras
        self.nombreProducto = nombreProducto
        self.descripcion = descripcionProducto
        self.idDependiendoCategoria = idDependiendoCategoria
        self.nombreDependiendoCategoria = nombreDependiendoCategoria
        self.IDPromocionTablaVarianteDeCategoria = IDPromocionTablaVarianteDeCategoria
        self.IDPromocion = IDPromocion
        self.NombrePromocion = NombrePromocion
        self.Descuento = Descuento
        self.Impresa = Impresa
        self.IDHorarioPromocion = IDHorarioPromocion
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.LimitePorCliente = LimitePorCliente
        self.imagenes = imagenes
        self.precio = precio
        self.PrecioPromocion = PrecioPromocion
        self.puntuacion = puntuacion
        self.tieneEnvio = tieneEnvio
        self.costoEnvio = costoEnvio
        self.estaEnProductoFavorito = estaEnProductoFavorito
        self.mostrarInteraccion = mostrarInteraccion
