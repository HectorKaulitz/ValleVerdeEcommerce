class getsetObjetoCarrito:
    objetoCarritoUsuario = None
    objFavoritos = None
    EsParaFavoritos = False

    def __init__(self, objetoCarritoUsuario, objFavoritos, EsParaFavoritos):
        self.objetoCarritoUsuario = objetoCarritoUsuario
        self.objFavoritos = objFavoritos
        self.EsParaFavoritos = EsParaFavoritos