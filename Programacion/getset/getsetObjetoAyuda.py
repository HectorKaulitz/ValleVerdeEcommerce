class getsetObjetoAyuda:
    controlador = None
    busqueda = ""
    temas = []

    def __init__(self, controlador, busqueda, temas):
        self.controlador = controlador
        self.busqueda = busqueda
        self.temas = temas