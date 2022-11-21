class getsetDireccion:
    idDireccion = ""
    idUsuarioRegistrado = ""
    ciudad = ""
    colonia = ""
    calle = ""
    numeroExterior = ""
    numeroInterior = ""
    destinatario = ""
    preferida = False
    pais = ""
    iso3Pais = ""
    estado = ""
    codigoEstado = ""
    codigoPostal = ""

    def __init__(self, idDireccion, idUsuarioRegistrado, ciudad, colonia, calle, numeroExterior,
                 numeroInterior, destinatario, preferida, pais, iso3Pais, estado, codigoEstado,
                 codigoPostal):
        self.idDireccion = idDireccion
        self.idUsuarioRegistrado = idUsuarioRegistrado
        self.ciudad = ciudad
        self.colonia = colonia
        self.calle = calle
        self.numeroExterior = numeroExterior
        self.numeroInterior = numeroInterior
        self.destinatario = destinatario
        self.preferida = preferida
        self.pais = pais
        self.iso3Pais = iso3Pais
        self.estado = estado
        self.codigoEstado = codigoEstado
        self.codigoPostal = codigoPostal