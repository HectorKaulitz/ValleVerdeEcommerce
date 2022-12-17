from Programacion.Funcionalidad.Encriptacion import Encriptacion



class getsetObjetoProcesoCompra:

    def __init__(self, idUsuarioEncriptado,tipoPagos, controlador,productosCarrito,paqueteriaHabilitada,envioADomicilioPorDefecto,tipoPago,totalesCarrito):
        self.idUsuarioEncriptado = idUsuarioEncriptado
        self.controlador = controlador
        self.productosCarrito = productosCarrito
        self.paqueteriaHabilitada = paqueteriaHabilitada
        self.tipoPagos = tipoPagos
        self.envioADomicilioPorDefecto = envioADomicilioPorDefecto
        self.tipoPago = tipoPago
        self.totalesCarrito = totalesCarrito

