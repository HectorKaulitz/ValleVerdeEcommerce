class getsetObjetoComentario:
    controlador = None
    busqueda = ""
    comentarios = []
    usuario = None

    def __init__(self, controlador, busqueda, comentarios, usuario):
        self.controlador = controlador
        self.busqueda = busqueda
        self.comentarios = comentarios
        self.usuario = usuario