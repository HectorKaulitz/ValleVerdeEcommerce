from Programacion.getset import getsetBadgeFlotante


class getsetContenedorUsuario:

    usuario: getsetUsuarioRegistrado = None
    totalesBadgeFlotantes: getsetBadgeFlotante = None

    def __init__(self, usuario: getsetUsuarioRegistrado, totalesBadgeFlotantes: getsetBadgeFlotante):
        self.usuario = usuario
        self.totalesBadgeFlotantes = totalesBadgeFlotantes