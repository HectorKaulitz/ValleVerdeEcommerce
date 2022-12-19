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

    def ValidarNombreApellidosUsuario(self, nombre:str):
        continuar = True
        res = -3
        if nombre is None or nombre == "":
            res = -2
        else:
            for caracter in nombre:
                if caracter != " ":
                    if ord(caracter) >= 65 and ord(caracter) <=90:
                        continuar = True
                    else:
                        if ord(caracter) >= 97 and ord(caracter) <=122:
                            continuar = True
                        else:
                            continuar = False
                else:
                    continuar = True
            if continuar:
                res = 1
            else:
                res = -1
        #   1 todo bien
        #   -1 caracteres invalidos
        #   -2 vacio
        #   -3 error metodos
        return res

    def ValidarCorreoUsuario(self, correo:str, modificacion:bool, request):
        continuar = True
        idUsuario = -1
        res = -3
        if correo is None or correo == "":
            res = -2
        else:
            if modificacion:
                usuario = self.ObtenerUsuarioDeLaSesionActual(request)
                if usuario is not None:
                    idUsuario = usuario.IDUsuarioRegistrado
            resB = MySQL().ExisteCorreoUsuario(correo, idUsuario)
            if resB == -1:
                res = -4
            else:
                res = 1
        return res

    def ValidarTelefonoUsuario(self, telefono, modificacion, request):
        continuar = True;
        idUsuario = "-1";
        res = -3;
        if telefono is None or telefono == "":
            res = 1
        else:
            index = 0
            for caracter in telefono:
                if ord(caracter) >= 48 and ord(caracter) <= 57:
                    continuar = True
                else:
                    if caracter=="+" and index == 0:
                        continuar = True
                    else:
                        continuar = False
                index+=1
            if continuar:
                if modificacion:
                    usuario = self.ObtenerUsuarioDeLaSesionActual(request)
                    if usuario is not None:
                        idUsuario = usuario.IDUsuarioRegistrado
                resB = MySQL().ExisteTelefono(telefono, idUsuario)
                if resB == -1:
                    res = -4
                else:
                    res = 1
        return res

    def ValidarUsuario(self, usuario:str, modificacion:bool, request):
        continuar = True
        longitudMinima = 8
        longitudMaxima = 20
        idUsuario = "-1"
        res = -3
        if usuario is None or usuario == "":
            res = -2
        else:
            if (len(usuario) >= longitudMinima):
                if (len(usuario) <= longitudMaxima):
                    for caracter in usuario:
                        if ord(caracter) >= 65 and ord(caracter) <=90:
                            continuar = True
                        else:
                            if ord(caracter) >= 97 and ord(caracter) <=122:
                                continuar = True
                            else:
                                if ord(caracter) >= 48 and ord(caracter) <= 57:
                                    continuar = True
                                else:
                                    if caracter=="-" or caracter=="_":
                                        continuar = True
                                    else:
                                        continuar = False

                    if continuar:
                        if modificacion:
                            datosUsuario = self.ObtenerUsuarioDeLaSesionActual(request)
                            if datosUsuario is not None:
                                idUsuario = datosUsuario.IDUsuarioRegistrado
                        resB = MySQL().ExisteUsuario(usuario, idUsuario)
                        if resB == -1:
                            res = -6
                        else:
                            res = 1
                else:
                    res = -5
            else:
                res = -4
        return res

    def ValidarContraseñaUsuario(self, contraseña):
        continuar = True
        longitudMinima = 8
        longitudMaxima = 25
        res = -3
        contieneLetras = False
        contieneNumeros = False
        cumpleLongitud = True
        if contraseña is None or contraseña == "":
            res = -2
        else:
            if (len(contraseña) >= longitudMinima):
                if (len(contraseña) <= longitudMaxima):
                    for caracter in contraseña:
                        if ord(caracter) >= 65 and ord(caracter) <=90:
                            contieneLetras = True;
                            continuar = True
                        else:
                            if ord(caracter) >= 97 and ord(caracter) <=122:
                                contieneLetras = True;
                                continuar = True
                            else:
                                if ord(caracter) >= 48 and ord(caracter) <= 57:
                                    contieneNumeros = True;
                                    continuar = True
                                else:
                                    continuar = False
                    if continuar:
                        if contieneLetras:
                            if contieneNumeros:
                                res = 1
                            else:
                                res = -7
                        else:
                            res = -6
                    else:
                        res = -1
                else:
                    cumpleLongitud = False
                    res = -5
            else:
                cumpleLongitud = False
                res = -4
        return res

    def ValidarConfirmarContraseñaUsuario(self, contraseña, contraseñaConfirmar):
        res = -3
        if contraseña is None or contraseñaConfirmar is None or contraseña  == "" or contraseñaConfirmar == "":
            res = -2
        else:
            if contraseña == contraseñaConfirmar:
                res = 1
            else:
                res = -1
        return res

    def ValidarContraseñaActualUsuario(self, contraseña, request, mySql):

        longitudMinima = 8
        longitudMaxima = 25
        res = -3
        if contraseña is None or contraseña == "":
            res = -2
        else:
            if len(contraseña) >= longitudMinima:
                if len(contraseña) <= longitudMaxima:
                    idUsuario = "-1"
                    datosUsuario = self.ObtenerUsuarioDeLaSesionActual(request)
                    if datosUsuario is not None:
                        idUsuario = datosUsuario.IDUsuarioRegistrado
                    res = mySql.CoincideContraseñaActualUsuario(contraseña, idUsuario)
                else:
                    res = -5
            else:
                res = -4
        return res