from flask import make_response, render_template


class Utileria:

    def RedondeoDouble(self, cifra):
        try:
            d = float(cifra)
            d = round(d, 2)
        except Exception:
            d = 0
        return d

    def ObtenerUsuarioDeLaSesionActual(self, request):
        cookie = request.cookies.get('SesionUsuario')
        return cookie

    def EliminarCookie(self, template):
        resp = make_response(render_template(template))
        resp.delete_cookie('SesionUsuario')

    def VerificarCookie(self, nombreCookie):
        valor = None  # controlador.Request.Cookies[nombreCookie];
        if valor is not None:
            return valor;
        else:
            return "";