class getsetDepartamentoMarca:

    idDepartamentoMarca = ""
    idDepartamento = ""
    idMarca = ""
    puntuacion = 0
    nombre = ""
    tipo = 0
    tipoEncritado = ""

    def __init__(self, idDepartamentoMarca, idDepartamento, idMarca, puntuacion, nombre, tipo, tipoEncritado):
        self.idDepartamentoMarca = idDepartamentoMarca
        self.idDepartamento = idDepartamento
        self.idMarca = idMarca
        self.puntuacion = puntuacion
        self.nombre = nombre
        self.tipo = tipo
        self.tipoEncritado = tipoEncritado