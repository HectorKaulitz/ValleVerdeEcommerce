from flask import make_response, render_template

from MySqlConexion import MySQL
from Programacion.getset import getsetUsuarioRegistrado


class Utileria:

    def RedondeoDouble(self, cifra):
        try:
            d = float(cifra)
            d = round(d, 2)
        except Exception:
            d = 0
        return d

    def ObtenerUsuarioDeLaSesionActual(self, request):
        cookie: bytearray = request.cookies.get('SesionUsuario')

        if( cookie is not None):
            b = bytearray()
            b.extend(map(ord, cookie))

            mySql = MySQL();
            datosUsuario:getsetUsuarioRegistrado = mySql.ObtenerUsuarioPorToken(b);

            return datosUsuario
        else:
            return None

    def EliminarCookie(self):
        resp = make_response("Cookie Removed")
        resp.set_cookie('SesionUsuario', '', expires=0)
        resp.delete_cookie('SesionUsuario')

    def VerificarCookie(self, nombreCookie):
        valor = None  # controlador.Request.Cookies[nombreCookie];
        if valor is not None:
            return valor;
        else:
            return "";