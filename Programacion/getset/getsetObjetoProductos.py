from Programacion.getset.getsetInformacionCarousel import getsetInformacionCarousel


class getsetObjetoProductos:

    def __init__(self, productosResultado, productosCarousel, Filtros, informacion, controlador, busqueda, usuario,
                 detectionService):
        self.productosResultado = productosResultado;
        self.informacionCarousel = getsetInformacionCarousel(detectionService, productosCarousel, usuario);
        self.Filtros = Filtros;
        self.Informacion = informacion;
        self.controlador = controlador;
        self.busqueda = busqueda;
        self.usuario = usuario;
        self.detectionService = detectionService;