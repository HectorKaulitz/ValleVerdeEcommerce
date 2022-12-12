from Programacion.getset import getsetUsuarioRegistrado, getsetTotalesCarrito, getsetBadgeFlotante


class getsetInformacionCabecera:
    listaCategorias = []
    listaDepartamentos = []
    listaProductosCarrito = []
    usuario: getsetUsuarioRegistrado = None
    mostrarTodoCabecera = False
    busqueda = ""
    mostrarCarrito = False
    totalCarrito: getsetTotalesCarrito = None
    totalesBadgeFlotantes: getsetBadgeFlotante = None

    def __init__(self, listaCategorias, listaDepartamentos, listaProductosCarrito, usuario,
                 mostrarTodoCabecera, busqueda, mostrarCarrito, totalCarrito, totalesBadgeFlotantes):
        self.listaCategorias = listaCategorias
        self.listaDepartamentos = listaDepartamentos
        self.listaProductosCarrito = listaProductosCarrito
        self.usuario = usuario
        self.mostrarTodoCabecera = mostrarTodoCabecera
        self.busqueda = busqueda
        self.mostrarCarrito = mostrarCarrito
        self.totalCarrito = totalCarrito
        self.totalesBadgeFlotantes = totalesBadgeFlotantes