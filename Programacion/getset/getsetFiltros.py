class getsetFiltros:

    id = ""
    nombre = ""
    nombreCategoria = ""
    tipoCategoria = 0
    tieneSubFiltros = False

    def __init__(self, id, nombre, nombreCategoria, tipoCategoria, tieneSubFiltros,idFiltro):
        self.id = id
        self.nombre = nombre
        self.nombreCategoria = nombreCategoria
        self.tipoCategoria = tipoCategoria
        self.tieneSubFiltros = tieneSubFiltros
        self.idFiltro = idFiltro