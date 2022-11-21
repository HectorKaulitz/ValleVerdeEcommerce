class getsetDepartamentoLinea:
    idDepartamentoLinea = ""
    idDepartamento = ""
    idLinea = ""
    puntuacion = 0
    nombre = ""
    tipo = 0
    tipoEncritado = ""

    def __init__(self, idDepartamentoLinea, idDepartamento, idLinea, puntuacion, nombre, tipo, tipoEncritado):
        self.idDepartamentoLinea = idDepartamentoLinea
        self.idDepartamento = idDepartamento
        self.idLinea = idLinea
        self.puntuacion = puntuacion
        self.nombre = nombre
        self.tipo = tipo
        self.tipoEncritado = tipoEncritado