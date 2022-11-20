class getsetDepartamento:

    idDepartamento:str = ""
    nombreDepartamento:str = ""
    fecha:str = ""
    activo:bool = False
    departamentosLineas = []
    departamentoMarcas = []

    def __init__(self, idDepartamento, nombre, fecha, activo, departamentosLineas, departamentoMarcas):
        self.idDepartamento = idDepartamento
        self.nombreDepartamento = nombre
        self.fecha = fecha
        self.activo = activo
        self.departamentosLineas = departamentosLineas
        self.departamentoMarcas = departamentoMarcas