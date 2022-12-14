class getsetComentario:
    pos = -1
    idComentario = ""
    idUsuario = ""
    nombreUsuario = ""
    tema = ""
    comentario = ""
    fechaCreacion = ""
    fechaUltimaModificacion = ""
    activo = False
    respuestas = []

    def __init__(self, pos, idComentario, idUsuario, nombreUsuario, apellidoUsuario, tema,
                 comentario, fechaCreacion, fechaUltimaModificacion, activo, respuestas):
        self.pos = pos
        self.idComentario = idComentario
        self.idUsuario = idUsuario
        self.nombreUsuario = nombreUsuario + " " + apellidoUsuario
        self.tema = tema
        self.comentario = comentario
        self.fechaCreacion = fechaCreacion
        self.fechaUltimaModificacion = fechaUltimaModificacion
        self.activo = activo
        self.respuestas = respuestas
