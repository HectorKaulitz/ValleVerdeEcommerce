from Programacion.Funcionalidad.Encriptacion import Encriptacion
import json


class getsetSugerenciaBusqueda:
    oben = Encriptacion()

    def __init__(self, idProducto, codigoBarras, nombreProducto):
        self.idProducto = idProducto
        self.codigoBarras = codigoBarras
        self.nombreProducto = nombreProducto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
