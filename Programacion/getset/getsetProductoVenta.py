



class getsetProductoVenta:

    def __init__(self, indice, idVenta, idUsuario, idProductoVenta, idProducto,nombre,descripcion,bloqueado,cantidadPedida,costoAlMomentoVenta,precioAlMomentoVenta
                 ,precioCobrado,existencia,cantidadSurtida):
        from Programacion.Funcionalidad.Utileria import Utileria
        self.indice = indice
        self.idVenta = idVenta
        self.idUsuario = idUsuario
        self.idProductoVenta = idProductoVenta
        self.idProducto = idProducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.bloqueado = bloqueado
        self.cantidadPedida = Utileria().RedondeoDouble(cantidadPedida)
        self.costoAlMomentoVenta = Utileria().RedondeoDouble(costoAlMomentoVenta)
        self.precioAlMomentoVenta = Utileria().RedondeoDouble(precioAlMomentoVenta)
        self.precioCobrado = Utileria().RedondeoDouble(precioCobrado)
        self.existencia =Utileria().RedondeoDouble(existencia)
        self.cantidadSurtida = Utileria().RedondeoDouble(cantidadSurtida)
