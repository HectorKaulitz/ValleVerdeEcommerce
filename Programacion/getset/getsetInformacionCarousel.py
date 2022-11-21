class getsetInformacionCarousel:
    detectionService = None
    productosCarousel = []
    usuario = None

    def __init__(self, detectionService, productosCarousel, usuario):
        self.detectionService = detectionService
        self.productosCarousel = productosCarousel
        self.usuario = usuario