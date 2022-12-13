from flask import Flask, render_template, Blueprint, request
from flask_cors import CORS

from MySqlConexion import MySQL
from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.Utileria import Utileria
from Programacion.getset import getsetUsuarioRegistrado
from Programacion.getset.getsetBadgeFlotante import getsetBadgeFlotante
from Programacion.getset.getsetInformacionCabecera import getsetInformacionCabecera
from Programacion.getset.getsetInformacionCarousel import getsetInformacionCarousel
from Programacion.getset.getsetObjetoAyuda import getsetObjetoAyuda
from Programacion.getset.getsetObjetoComentario import getsetObjetoComentario
from Programacion.getset.getsetObjetoPaginaInicio import getsetObjetoPaginaInicio
from Programacion.getset.getsetObjetoProducto import getsetObjetoProducto
from Programacion.getset.getsetObjetoPromociones import getsetObjetoPromociones
from Programacion.getset.getsetResultado import getsetResultado
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
    informacionCabecera = LlenarCabecera(True, "")
    # ----------------------------
    objetoInicio = getsetObjetoPaginaInicio("index", productosOfertaCarousel, productosDestacadosCarousel,
                                            productosNuevosCarousel, informacionCabecera)
    return render_template('Index.html', objetoInicio=objetoInicio, informacionCabecera=informacionCabecera)


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

    # if (_detectionService.Device.Type == Device.Mobile)
    #   numeroCuadrosPagina = 4;

    productosPromocion = mySql.ObtenerProductosDePromocionPorCategoria(2);

    productosPromocionIndividuales = mySql.ObtenerProductosDePromocionPorCategoria(-1, numeroPagina, productosPagEnc);

    NumeroTotalProductos = mySql.ObtenerNumeroPaginasProductosDePromocionPorCategoria(-1, productosPagEnc);
    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request);

    informacionCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(2), datosUsuario);
    objetoPromociones = getsetObjetoPromociones("", informacionCarousel, productosPromocion,
                                                productosPromocionIndividuales,
                                                numeroPagina, productosPagEnc, numeroCuadrosPagina,
                                                NumeroTotalProductos);

    return render_template('promociones.html', objetoPromociones=objetoPromociones)


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
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, busqueda)
    # ----------------------------
    informacion = getsetObjetoProducto(None, busqueda, productosCarousel, productoSeleccionado, None, datosUsuario,
                                       informacionCabecera)
    return render_template('Producto.html', informacion=informacion)


@app.route('/comentarios')
def comentarios():
    mysql = MySQL()
    usuario: getsetUsuarioRegistrado = None  # falta obtener el usuario
    comentarios = []
    if usuario is not None:
        comentarios = mysql.ObtenerComentarioUsuario(usuario.IDUsuarioRegistrado)
        objetoComentario = getsetObjetoComentario(None, "", comentarios, usuario)
    return render_template('comentarios.html', objetoComentario=objetoComentario)


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
    mysql = MySQL()
    temas = mysql.ObtenerTemasAyuda();
    objetoAyuda = getsetObjetoAyuda(None, "", temas);
    return render_template('ayuda.html', temas)


@app.route('/perfilUsuario')
def perfilUsuario():
    return render_template('perfilUsuario.html')


def _validarUsuarioInicioSesion(usuario):
    res: int = -3;
    longitudMinima: int = 8;
    longitudMaxima: int = 20;

    continuar: bool = True;

    if (usuario == None):
        res = -2;
    else:
        caracteres = list();
        caracteres.extend(usuario);

        if (len(caracteres) >= longitudMinima):
            if (len(caracteres) <= longitudMaxima):
                for caracter in caracteres:
                    if (ord(caracter) >= 65 and ord(caracter) <= 90):
                        # caracteres A-Z MAYUSCULAS CODIGO ASCII
                        continuar = True;
                    else:
                        if (ord(caracter) >= 97 and ord(caracter) <= 122):
                            # caracteres a-z minusculas CODIGO ASCII
                            continuar = True;
                        else:
                            if (ord(caracter) >= 48 and ord(caracter) <= 57):
                                # caracteres 0-9 CODIGO ASCII
                                continuar = True;
                            else:
                                if ((caracter + "") == ("-") or (caracter + "") == ("_")):
                                    # guiones
                                    continuar = True;
                                else:
                                    # encontro otro caracter
                                    continuar = False;
                                    break;

                if (continuar):
                    mySql = MySQL()
                    resB: int = mySql.ExisteUsuario(usuario);
                    if (resB == -1):  # si existe
                        res = 1;
                    else:  # esta disponible
                        res = -6;
                else:
                    res = -1;  # caracteres ivalidos
            else:
                res = -5;  # no cumple lo maximo
        else:
            res = -4;  # no cumple lo minimo

            # 1 existe usuario
            # -1caracteres ivalidos
            # -2 vacio
            # -3 error metodo
            # -4longitud minima
            # -5 longitud maxima
            # -6 no existe
    return getsetResultado(res, '', '', '');


def _validarContrasenaInicioSesion(contrasena):
    # contrasena = contrasena.Trim();
    res: int = -3;
    longitudMinima: int = 8;
    longitudMaxima: int = 25;

    contieneLetras = False;
    contieneNumeros = False;
    cumpleLongitud = True;
    continuar = True;

    if (contrasena == None):
        res = -2;  # vacio
    else:
        # contraseña = contraseña.Trim();
        caracteres = list();
        caracteres.extend(contrasena);
        if (len(caracteres) >= longitudMinima):
            if (len(caracteres) <= longitudMaxima):
                for caracter in caracteres:
                    if (ord(caracter) >= 65 and ord(caracter) <= 90):
                        # caracteres A-Z MAYUSCULAS CODIGO ASCII
                        contieneLetras = True;
                        continuar = True;
                    else:
                        if (ord(caracter) >= 97 and ord(caracter) <= 122):
                            # caracteres a-z minusculas CODIGO ASCII
                            contieneLetras = True;
                            continuar = True;
                        else:
                            if (ord(caracter) >= 48 and ord(caracter) <= 57):
                                # caracteres 0-9 CODIGO ASCII
                                contieneNumeros = True;
                                continuar = True;
                            else:
                                # encontro otro caracter
                                continuar = False;
                                break;
                if (continuar):
                    if (contieneLetras):
                        if (contieneNumeros):
                            res = 1;
                        else:
                            res = -7;
                    else:
                        res = -6;
                else:
                    res = -1;  # caracteres ivalidos
            else:
                cumpleLongitud = False;
                res = -5;  # no cumple lo maximo
        else:
            cumpleLongitud = False;
            res = -4;  # no cumple lo minimo

    # 1 todo bien
    # -1caracteres ivalidos
    # -2 vacio
    # -3 error metodo
    # -4longitud minima
    # -5 longitud maxima
    # -6 no contiene letras
    # -7 no contiene numeros
    return getsetResultado(res, '', '', '');


@app.route('/validarDatosInicioSesion/', methods=['POST', 'GET'])
def validarDatosInicioSesion():
    res: int = -3;

    mySql = MySQL()
    usuario = request.form['usuario'];
    contrasena = request.form['contrasena'];
    resultU: int = _validarUsuarioInicioSesion(usuario).resultado;
    resultC: int = _validarContrasenaInicioSesion(contrasena).resultado;

    if ((resultU == 1 or resultU == -6) and resultC == 1):
        res = mySql.ValidarDatosInicioSesion(usuario, contrasena);
        if (res == 1):
            sesion = mySql.AgregarSesionUsuario(usuario);
            return jsonify({"resultado": res, "idSesion": sesion[0], "token": sesion[1], "fechaExpiracion": sesion[2]});
    else:
        res = 2;

    # 1 coincide y esta activo
    # 2 debe pasar la validacion de campos
    # -1 usuario no existe
    # -2 usuario existe,contraseña mal
    # -3 erro metodo/proced
    # -4 cuenta inactiva

    return jsonify({"resultado": res, "idSesion": "", "token": "", "fechaExpiracion": ""})

@app.route('/validarUsuarioInicioSesion/', methods=['POST', 'GET'])
def validarUsuarioInicioSesion():

    usuario = request.form['usuario'];

    res = _validarUsuarioInicioSesion(usuario);

    return jsonify({"resultado": res.resultado, "idSesion": res.idSesion, "token": res.token, "fechaExpiracion": res.fechaExpiracion})

@app.route('/validarContrasenaInicioSesion/', methods=['POST', 'GET'])
def validarContrasenaInicioSesion():

    contrasena = request.form['contrasena'];

    res = _validarContrasenaInicioSesion(contrasena);

    return jsonify({"resultado": res.resultado, "idSesion": res.idSesion, "token": res.token,
                    "fechaExpiracion": res.fechaExpiracion})


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
