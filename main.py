from flask import Flask, render_template, Blueprint, request
from flask_cors import CORS

from MySqlConexion import MySQL
from Programacion.Funcionalidad.Utileria import Utileria
from Programacion.getset.getsetBadgeFlotante import getsetBadgeFlotante
from Programacion.getset.getsetInformacionCabecera import getsetInformacionCabecera
from Programacion.getset.getsetInformacionCarousel import getsetInformacionCarousel
from Programacion.getset.getsetObjetoPaginaInicio import getsetObjetoPaginaInicio
from Programacion.getset.getsetObjetoPromociones import getsetObjetoPromociones
from Programacion.getset.getsetTotalesCarrito import getsetTotalesCarrito

index = Blueprint('index', __name__, url_prefix='/index', template_folder='Vistas')


# producto = Blueprint('producto', __name__, url_prefix='/producto', template_folder='Vistas')


def create_app():
    app = Flask(__name__)
    # configurar referencias cruzadas
    # cuando se hacen peticiones de otros dominios
    CORS(app)
    app.config.from_object('configuracion.DevConfig')
    # registrar blueprints
    app.register_blueprint(index)
    # app.register_blueprint(producto)
    # from .Productos import producto
    # app.register_blueprint(producto)
    return app


app = create_app()


# ruta principal
@app.route('/')
def index():
    mySql = MySQL()
    # if mySql.conectar_mysql():
    #     categorias = mySql.ObtenerCategoria()
    #     print(categorias)
    #     mySql.desconectar_mysql()

    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request=request)
    productosOfertaCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(1), datosUsuario)
    productosDestacadosCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(2), datosUsuario)
    productosNuevosCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(4), datosUsuario)
    objetoInicio = getsetObjetoPaginaInicio("index", productosOfertaCarousel, productosDestacadosCarousel,
                                            productosNuevosCarousel)

    # cabecera = LlenarCabecera(True, "")

    return render_template('Index.html', objetoInicio=objetoInicio)


@app.route('/productos')
def productos():
    return render_template('productos.html')


@app.route('/historialCompras')
def historialCompras():
    return render_template('historialCompras.html')


@app.route('/promociones')
def promociones():
    mySql = MySQL()
    productosPagEnc = 10
    numeroPagina = 0

    if (productosPagEnc == -2):
        productosPagEnc = 10

    numeroCuadrosPagina = 5

    #if (_detectionService.Device.Type == Device.Mobile)
    #   numeroCuadrosPagina = 4;

    productosPromocion = mySql.ObtenerProductosDePromocionPorCategoria(2);

    productosPromocionIndividuales = mySql.ObtenerProductosDePromocionPorCategoria(-1, numeroPagina, productosPagEnc);

    NumeroTotalProductos = mySql.ObtenerNumeroPaginasProductosDePromocionPorCategoria(-1, productosPagEnc );
    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request);

    informacionCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(2), datosUsuario);
    objetoPromociones = getsetObjetoPromociones( "", informacionCarousel, productosPromocion, productosPromocionIndividuales,
                                numeroPagina, productosPagEnc , numeroCuadrosPagina, NumeroTotalProductos);

    return render_template('promociones.html', objetoPromociones = objetoPromociones)


@app.route('/iniciarSesion')
def iniciarSesion():
    return render_template('iniciarSesion.html')


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')


@app.route('/producto')
def producto():
    return render_template('Producto.html')


@app.route('/comentarios')
def comentarios():
    return render_template('comentarios.html')


@app.route('/carritoUsuario')
def carrito():
    return render_template('carritoUsuario.html', EsParaFavoritos=False)


@app.route('/favorito')
def favorito():
    return render_template('carritoUsuario.html', EsParaFavoritos=True)


@app.route('/procesoCompra')
def procesoCompra():
    return render_template('procesoCompra.html')


@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')


@app.route('/perfilUsuario')
def perfilUsuario():
    return render_template('perfilUsuario.html')


def LlenarCabecera(mostrar: bool, busqueda: str, mostrarCarrito=True, template=""):
    informacion = None
    cookieSesion = None
    datosUsuario = None
    token = None
    if mostrar:
        mySql = MySQL()
        datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
        productosCarrito = []
        totalCarrito = getsetTotalesCarrito()
        totalesBadgeFlotantes = getsetBadgeFlotante(0, 0, 0)
        if datosUsuario is None:
            Utileria().EliminarCookie(template)
        else:
            productosCarrito = mySql.ObtenerProductosCarritoUsuario(datosUsuario.IDUsuarioRegistrado)
            totalCarrito = mySql.ObtenerTotalesCarritoUsuario(datosUsuario.IDUsuarioRegistrado)
            totalesBadgeFlotantes = mySql.ObtenerTotalesParaBadgeFlotantes(datosUsuario.IDUsuarioRegistrado)

        categorias = mySql.ObtenerCategoria()
        departamentos = mySql.ObtenerDepartamentos()
        informacion = getsetInformacionCabecera(categorias, departamentos, productosCarrito, datosUsuario, mostrar,
                                                busqueda, mostrarCarrito, totalCarrito, totalesBadgeFlotantes)
    else:
        informacion = getsetInformacionCabecera(None, None, None, None, mostrar, "", mostrarCarrito, None, None)
    return informacion

#
# if __name__ == '__main__':
#     print(__name__)
#     app.run()
