from Programacion.getset import getsetBadgeFlotante
from Programacion.getset.getsetUsuarioRegistrado import getsetUsuarioRegistrado


class getsetContenedorUsuario:

    usuario: getsetUsuarioRegistrado = None
    totalesBadgeFlotantes: getsetBadgeFlotante = None

    def __init__(self, usuario: getsetUsuarioRegistrado, totalesBadgeFlotantes: getsetBadgeFlotante):
        self.usuario = usuario
        self.totalesBadgeFlotantes = totalesBadgeFlotantes