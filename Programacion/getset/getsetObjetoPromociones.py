from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.Utileria import Utileria


class getsetObjetoPromociones:
    obu = Utileria()
    oben = Encriptacion()

    def __init__(self, busqueda, informacionCarousel, productosPromocion, productosPromocionIndividuales, numeroPagina,
                 productosPag, numeroCuadrosPagina, NumeroTotalProductos,informacionCabecera):
        self.busqueda = busqueda
        self.informacionCarousel = informacionCarousel
        self.productosPromocion = productosPromocion
        self.productosPromocionIndividuales = productosPromocionIndividuales
        self.numeroPagina = numeroPagina
        self.productosPag = productosPag
        self.numeroCuadrosPagina = numeroCuadrosPagina
        self.NumeroTotalProductos = NumeroTotalProductos
        self.informacionCabecera = NumeroTotalProductos
