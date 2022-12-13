from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.Utileria import Utileria
import json

class getsetResultado:

    def __init__(self, res, idSesion, token, fechaExpiracion):
        self.resultado = res
        self.idSesion = idSesion
        self.token = token
        self.fechaExpiracion = fechaExpiracion

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

