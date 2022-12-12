from flask import Flask, render_template, Blueprint, request
from flask_cors import CORS

from MySqlConexion import MySQL
from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.Utileria import Utileria
from Programacion.getset.getsetBadgeFlotante import getsetBadgeFlotante
from Programacion.getset.getsetInformacionCabecera import getsetInformacionCabecera
from Programacion.getset.getsetInformacionCarousel import getsetInformacionCarousel
from Programacion.getset.getsetObjetoPaginaInicio import getsetObjetoPaginaInicio
from Programacion.getset.getsetObjetoProducto import getsetObjetoProducto
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


# ruta principal
@app.route('/')
def index():
    mySql = MySQL()
    # if mySql.conectar_mysql():
    #     categorias = mySql.ObtenerCategoria()
    #     print(categorias)
    #     mySql.desconectar_mysql()

    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request=request)
    productosOfertaCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(1),
                                                        datosUsuario)
    productosDestacadosCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(2),
                                                            datosUsuario)
    productosNuevosCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(4),
                                                        datosUsuario)
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, "", "Index.html")
    # ----------------------------
    objetoInicio = getsetObjetoPaginaInicio("index", productosOfertaCarousel, productosDestacadosCarousel,
                                            productosNuevosCarousel, informacionCabecera)



    return render_template('Index.html', objetoInicio=objetoInicio)


@app.route('/productos')
def productos():
    return render_template('productos.html')


@app.route('/historialCompras')
def historialCompras():
    return render_template('historialCompras.html')


@app.route('/promociones')
def promociones():
    return render_template('promociones.html')


@app.route('/iniciarSesion')
def iniciarSesion():
    return render_template('iniciarSesion.html')


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')


@app.route('/producto')
def producto(tipo=-1, busqueda="", idProducto=""):
    mySql = MySQL();
    idProductoDes = Encriptacion().Decrypt(idProducto);
    productosCarousel = mySql.ObtenerProductosCarouselPorCategoria(3, idProductoDes);
    productoSeleccionado = mySql.ObtenerProducto(idProductoDes);
    token = Utileria().VerificarCookie("SesionUsuario");
    datosUsuario = mySql.ObtenerUsuarioPorToken(token);
    #cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, busqueda, "producto.html")
    #----------------------------
    informacion = getsetObjetoProducto(None, busqueda, productosCarousel, productoSeleccionado, None, datosUsuario, informacionCabecera)
    return render_template('Producto.html', informacion=informacion)


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



#
# if __name__ == '__main__':
#     print(__name__)
#     app.run()
