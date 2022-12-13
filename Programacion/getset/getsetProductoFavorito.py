


class getsetProductoFavorito:

    def __init__(self, indice, IDProductoFavorito, IDProducto, CodigoBarras, Nombre, Descripcion, ExistenciaTotalProducto,
                 IDUsuarioRegistrado, FechaAgrego, PrecioAgregado, PrecioPromocion, Precio, Bloqueado, imagenes,
                 IDProductoFavoritoEncriptado, mostrarInteraccion):
        from Programacion.Funcionalidad.Utileria import Utileria
        from Programacion.Funcionalidad.Encriptacion import Encriptacion
        self.indice = indice
        self.IDProductoFavorito = IDProductoFavorito
        self.IDProducto = IDProducto
        self.CodigoBarras = CodigoBarras
        self.Nombre = Nombre
        self.Descripcion = Descripcion
        self.ExistenciaTotalProducto = Utileria().RedondeoDouble(ExistenciaTotalProducto)
        self.IDUsuarioRegistrado = IDUsuarioRegistrado
        self.FechaAgrego = FechaAgrego
        self.PrecioAgregado = Utileria().RedondeoDouble(PrecioAgregado)
        self.PrecioPromocion = Utileria().RedondeoDouble(PrecioPromocion)
        self.Precio = Utileria().RedondeoDouble(Precio)
        self.DiferenciaConPrecioActual = Utileria().RedondeoDouble(PrecioPromocion-PrecioAgregado)
        self.Bloqueado = Bloqueado
        self.imagenes = imagenes
        self.IDProductoFavoritoEncriptado = Encriptacion().Encrypt(IDProductoFavoritoEncriptado)
        self.mostrarInteraccion = mostrarInteraccion