from Programacion.getset.getsetInformacionCarousel import getsetInformacionCarousel


class getsetObjetoCarritoUsuario:
    controlador = None
    busqueda = ""
    informacionCarousel = None
    productosCarritos = []
    datosUsuario = None
    totalesCarrito = None
    paqueteriaHabilitada = False

    def __init__(self, controlador, busqueda, productosCarousel, productosCarritos, datosUsuario,
                 totalesCarrito, paqueteriaHabilitada, detectionService, configuracionWeb):
        self.controlador = controlador
        self.busqueda = busqueda
        self.informacionCarousel = getsetInformacionCarousel(detectionService, productosCarousel, datosUsuario);
        self.productosCarritos = productosCarritos
        self.datosUsuario = datosUsuario
        self.totalesCarrito = totalesCarrito
        self.paqueteriaHabilitada = paqueteriaHabilitada
        self.configuracionWeb = configuracionWeb
