class getsetIdentificacion:
    idIdentificacion = ""
    idUsuario = ""
    AprobadoFrontal = False
    AprobadoPosterior = False
    fechaAlta = ""
    fechaAprobadoFrontal = ""
    fechaAprobadoPosterior = ""
    imagenFrontal = []
    imagenPosterior = []

    def __init__(self, idIdentificacion, idUsuario, AprobadoFrontal, AprobadoPosterior, fechaAlta,
                 fechaAprobadoFrontal, fechaAprobadoPosterior, imagenFrontal,imagenPosterior):
        self.idIdentificacion = idIdentificacion
        self.idUsuario = idUsuario
        self.AprobadoFrontal = AprobadoFrontal
        self.AprobadoPosterior = AprobadoPosterior
        self.fechaAlta = fechaAlta
        self.fechaAprobadoFrontal = fechaAprobadoFrontal
        self.fechaAprobadoPosterior = fechaAprobadoPosterior
        self.imagenFrontal = imagenFrontal
        self.imagenPosterior = imagenPosterior