import json

from flask import Flask, render_template, Blueprint, request, jsonify
from flask_cors import CORS
from werkzeug.urls import url_encode

from MySqlConexion import MySQL
from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.Utileria import Utileria
from Programacion.getset import getsetUsuarioRegistrado
from Programacion.getset.getsetBadgeFlotante import getsetBadgeFlotante
from Programacion.getset.getsetInformacionCabecera import getsetInformacionCabecera
from Programacion.getset.getsetInformacionCarousel import getsetInformacionCarousel
from Programacion.getset.getsetInformacionGeneralProducto import getsetInformacionGeneralProducto
from Programacion.getset.getsetInformacionProductoCarrito import getsetInformacionProductoCarrito
from Programacion.getset.getsetObjetoAyuda import getsetObjetoAyuda
from Programacion.getset.getsetObjetoCarrito import getsetObjetoCarrito
from Programacion.getset.getsetObjetoCarritoUsuario import getsetObjetoCarritoUsuario
from Programacion.getset.getsetObjetoComentario import getsetObjetoComentario
from Programacion.getset.getsetObjetoDetallesVentaHistorial import getsetObjetoDetallesVentaHistorial
from Programacion.getset.getsetObjetoHistorialCompra import getsetObjetoHistorialCompra
from Programacion.getset.getsetObjetoPaginaInicio import getsetObjetoPaginaInicio
from Programacion.getset.getsetObjetoPerfilUsuario import getsetObjetoPerfilUsuario
from Programacion.getset.getsetObjetoProducto import getsetObjetoProducto
from Programacion.getset.getsetObjetoProductos import getsetObjetoProductos
from Programacion.getset.getsetObjetoProductosFavoritos import getsetObjetoProductosFavoritos
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


def LlenarCabecera(mostrar: bool, busqueda: str = "", mostrarCarrito=True):
    informacion = None
    cookieSesion = None
    datosUsuario = None
    token = None
    sNum = "10"
    if mostrar:
        mySql = MySQL()
        datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
        productosCarrito = []
        totalCarrito = getsetTotalesCarrito()
        totalesBadgeFlotantes = getsetBadgeFlotante(0, 0, 0)
        if datosUsuario is None:
            Utileria().EliminarCookie()
            intd = 4
        else:
            productosCarrito = mySql.ObtenerProductosCarritoUsuario(datosUsuario.IDUsuarioRegistrado)
            totalCarrito = mySql.ObtenerTotalesCarritoUsuario(productosCarrito)
            totalesBadgeFlotantes = mySql.ObtenerTotalesParaBadgeFlotantes(datosUsuario.IDUsuarioRegistrado)

        categorias = mySql.ObtenerCategoria()
        departamentos = mySql.ObtenerDepartamentos()
        informacion = getsetInformacionCabecera(categorias, departamentos, productosCarrito, datosUsuario, mostrar,
                                                busqueda, mostrarCarrito, totalCarrito, totalesBadgeFlotantes, sNum)
    else:
        informacion = getsetInformacionCabecera(None, None, None, None, mostrar, "", mostrarCarrito, None, None, sNum)
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


@app.route('/productos', methods=['POST', 'GET'])
def productos():
    oben = Encriptacion()
    mySql = MySQL()

    busqueda: str = request.args.get('busqueda', '')
    numeroPagina: int = int(request.args.get('numeroPagina', 0))
    productosPag = request.args.get('productosPag', 10)
    tipo = request.args.get('tipo', '-1')
    idMarca = request.args.get('idMarca', '-1')
    idLinea = request.args.get('idLinea', '-1')
    idFabricantes = request.args.get('idFabricantes', '-1')
    idDepartamento = request.args.get('idDepartamento', '-1')
    idSubLinea = request.args.get('idSubLinea', '-1')

    productosPagEnc = productosPag
    if productosPagEnc == -2:
        productosPagEnc = 10

    tipoEnc = tipo
    if tipoEnc == -2:
        tipoEnc = -1

    filtros = mySql.ObtenerFiltros(tipoEnc)

    productosResultado = mySql.ObtenerProductos(numeroPagina, productosPagEnc, idMarca, idLinea,
                                                idFabricantes, idDepartamento, busqueda, idSubLinea)

    productosCarousel = mySql.ObtenerProductosCarouselPorCategoria(2, "-1", idLinea, idMarca, idFabricantes, idSubLinea)

    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)

    numeroCuadrosPagina = 5

    informacion = getsetObjetoProductos(productosResultado, productosCarousel, filtros,
                                        getsetInformacionGeneralProducto(
                                            mySql.ObtenerNumeroPaginasProductos(productosPagEnc, idMarca, idLinea,
                                                                                idFabricantes, idDepartamento, busqueda,
                                                                                idSubLinea),
                                            tipoEnc, productosPagEnc, numeroCuadrosPagina), "productos", busqueda,
                                        datosUsuario, "Escritorio")

    informacionCabecera = LlenarCabecera(True, busqueda)
    patch = request.endpoint.split("/")

    return render_template('productos.html', informacionCabecera=informacionCabecera, informacion=informacion,
                           patch=patch, numeroPagina=numeroPagina)


@app.route('/historialCompras')
def historialCompras():
    mysql = MySQL()
    usuarioActual = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    ventas = []
    if usuarioActual is not None:
        ventas = mysql.ObtenerVentasUsuario(usuarioActual.IDUsuarioRegistrado, True, False)

    objetoHistorialCompras = getsetObjetoHistorialCompra(None, ventas)
    informacionCabecera = LlenarCabecera(True)

    return render_template('historialCompras.html', objetoHistorialCompras=objetoHistorialCompras,
                           informacionCabecera=informacionCabecera)


@app.route('/promociones', methods=['POST', 'GET'])
def promociones():
    mySql = MySQL()
    productosPag = request.args.get('productosPag', 10)
    numeroPagina: int = int(request.args.get('numeroPagina', 0)) - 1

    if (productosPag == -2):
        productosPag = 10

    numeroCuadrosPagina = 5

    # if (_detectionService.Device.Type == Device.Mobile)
    #   numeroCuadrosPagina = 4;

    productosPromocion = mySql.ObtenerProductosDePromocionPorCategoria(2);

    productosPromocionIndividuales = mySql.ObtenerProductosDePromocionPorCategoria(-1, numeroPagina, productosPag);

    NumeroTotalProductos = mySql.ObtenerNumeroPaginasProductosDePromocionPorCategoria(-1, productosPag);
    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request);

    informacionCarousel = getsetInformacionCarousel(None, mySql.ObtenerProductosCarouselPorCategoria(2), datosUsuario);
    informacionCabecera: getsetInformacionCabecera = LlenarCabecera(True, "");
    objetoPromociones = getsetObjetoPromociones("", informacionCarousel, productosPromocion,
                                                productosPromocionIndividuales,
                                                numeroPagina, productosPag, numeroCuadrosPagina,
                                                NumeroTotalProductos, informacionCabecera);

    return render_template('promociones.html', objetoPromociones=objetoPromociones, numeroPagina=numeroPagina)


@app.route('/iniciarSesion')
def iniciarSesion():
    informacionCabecera = LlenarCabecera(False, '')
    return render_template('iniciarSesion.html', informacionCabecera=informacionCabecera)


@app.route('/registrar')
def registrar():
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(False, "")
    # ----------------------------
    return render_template('registrar.html', informacionCabecera=informacionCabecera)


@app.route('/producto', methods=['POST', 'GET'])
def producto(tipo=-1, busqueda="", idProducto=""):
    patch = request.endpoint.split("/")
    idProducto = request.args['idProducto'];
    mySql = MySQL();

    productosCarousel = mySql.ObtenerProductosCarouselPorCategoria(3, idProducto);
    productoSeleccionado = mySql.ObtenerProducto(idProducto);
    token = Utileria().VerificarCookie("SesionUsuario");
    datosUsuario = mySql.ObtenerUsuarioPorToken(token);
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, busqueda)
    # ----------------------------
    informacionCarousel = getsetInformacionCarousel(None, productosCarousel, datosUsuario);
    informacion = getsetObjetoProducto(None, busqueda, productosCarousel, productoSeleccionado, None, datosUsuario,
                                       informacionCabecera, informacionCarousel)
    patch.append(productoSeleccionado.nombreProducto)
    return render_template('Producto.html', ObjetoProducto=informacion, patch=patch)


@app.route('/comentarios')
def comentarios():
    mysql = MySQL()
    objetoComentario = None
    usuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    comentarios = []
    if usuario is not None:
        comentarios = mysql.ObtenerComentarioUsuario(usuario.IDUsuarioRegistrado)
        objetoComentario = getsetObjetoComentario(None, "", comentarios, usuario)
        # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, "", False)
    # ----------------------------
    return render_template('comentarios.html', objetoComentario=objetoComentario,
                           informacionCabecera=informacionCabecera)


@app.route('/carritoUsuario')
def carrito(Favoritos=False):
    mysql = MySQL()
    objetoCarrito = None
    datosUsuario: getsetUsuarioRegistrado = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, "")
    # ----------------------------
    if datosUsuario is not None:
        productosCarritos = mysql.ObtenerProductosCarritoUsuario(datosUsuario.IDUsuarioRegistrado)
        totalCarrito = mysql.ObtenerTotalesCarritoUsuario(productosCarritos)
        productosCarousel = mysql.ObtenerProductosCarouselPorCategoria(2)
        objCarritoUsuario = getsetObjetoCarritoUsuario(None, "", productosCarousel, productosCarritos, datosUsuario,
                                                       totalCarrito,
                                                       False, None, mysql.ObtenerConfiguracionWeb())
        productosFavoritos = mysql.ObtenerProductosFavoritos(datosUsuario.IDUsuarioRegistrado)
        objFavoritos = getsetObjetoProductosFavoritos(productosFavoritos, datosUsuario)
        objetoCarrito = getsetObjetoCarrito(objCarritoUsuario, objFavoritos, Favoritos)

    return render_template('carritoUsuario.html', objetoCarrito=objetoCarrito, informacionCabecera=informacionCabecera,
                           EsParaFavoritos=False)


@app.route('/favorito')
def favorito():
    mysql = MySQL();
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, "")
    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    if datosUsuario is not None:
        productosCarritos = mysql.ObtenerProductosCarritoUsuario(datosUsuario.IDUsuarioRegistrado)
        totalCarrito = mysql.ObtenerTotalesCarritoUsuario(productosCarritos)
        productosCarousel = mysql.ObtenerProductosCarouselPorCategoria(2)
        objCarritoUsuario = getsetObjetoCarritoUsuario(None, "", productosCarousel, productosCarritos, datosUsuario,
                                                       totalCarrito,
                                                       False, None, mysql.ObtenerConfiguracionWeb())
        productosFavoritos = mysql.ObtenerProductosFavoritos(datosUsuario.IDUsuarioRegistrado)
        objFavoritos = getsetObjetoProductosFavoritos(productosFavoritos, datosUsuario)
        objetoCarrito = getsetObjetoCarrito(objCarritoUsuario, objFavoritos, True)
    # ----------------------------
    return render_template('carritoUsuario.html', EsParaFavoritos=True, informacionCabecera=informacionCabecera,
                           objetoCarrito=objetoCarrito)


@app.route('/procesoCompra')
def procesoCompra():
    return render_template('procesoCompra.html')


@app.route('/ayuda')
def ayuda():
    mysql = MySQL()
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True)
    # ----------------------------
    temas = mysql.ObtenerTemasAyuda();
    objetoAyuda = getsetObjetoAyuda(None, "", temas);
    return render_template('ayuda.html', objetoAyuda=objetoAyuda, informacionCabecera=informacionCabecera)


@app.route('/perfilUsuario')
def perfilUsuario():
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, "")
    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    # ----------------------------
    informacionUsuario = getsetObjetoPerfilUsuario(datosUsuario)
    return render_template('perfilUsuario.html', objetoPerfilUsuario=informacionUsuario,
                           informacionCabecera=informacionCabecera)


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

    return jsonify({"resultado": res.resultado, "idSesion": res.idSesion, "token": res.token,
                    "fechaExpiracion": res.fechaExpiracion})


@app.route('/validarContrasenaInicioSesion/', methods=['POST', 'GET'])
def validarContrasenaInicioSesion():
    contrasena = request.form['contrasena'];

    res = _validarContrasenaInicioSesion(contrasena);

    return jsonify({"resultado": res.resultado, "idSesion": res.idSesion, "token": res.token,
                    "fechaExpiracion": res.fechaExpiracion})


@app.route('/cerrarSesionUsuario/', methods=['POST', 'GET'])
def cerrarSesionUsuario():
    token = request.form['token'];

    mySql = MySQL();

    mySql.EliminarSesionUsuario(token);

    return jsonify({"res": "Sesion cerrada"}) \
 \
           @ app.route('/validarBusqueda/', methods=['POST', 'GET'])


def validarBusqueda():
    busqueda = request.form['busqueda'];

    res: int = -3;
    if (busqueda == None):
        busqueda = "";

    if (busqueda == ""):
        res = -1;
    else:
        res = 1;

    tipoEnc = "-1";
    numProductosPagina = "10";
    return jsonify({"resultado": res, "tipo": tipoEnc, "numero": numProductosPagina});


@app.route('/obtenerSugerenciasBusqueda/', methods=['POST', 'GET'])
def obtenerSugerenciasBusqueda():
    busqueda = request.form['busqueda'];

    sugerencias = []
    if (len(busqueda) > 0):
        mySql = MySQL();
        sugerencias = mySql.ObtenerSugerenciasBusqueda(busqueda);

    return jsonify(sugerencias)


@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))


@app.route('/AgregarProductoCarrito/', methods=['POST', 'GET'])
def AgregarProductoCarrito():
    idUsuario = request.form['idUsuario']
    idProducto = request.form['idProducto']
    cantidad = request.form['cantidad']

    mySql = MySQL()
    res = mySql.AgregarProductoCarritoUsuario(idUsuario, idProducto, cantidad)

    return jsonify({"resultado": res[0], "mensaje": res[1]})


@app.route('/ActualizarCantidadProductoCarrito/', methods=['POST', 'GET'])
def ActualizarCantidadProductoCarrito():
    idProductoCarrito = request.form['idProductoCarrito']
    cantidad = request.form['cantidad']
    tipo = request.form['tipo']
    idUsuario = request.form['idUsuario']

    mySql = MySQL()

    res: getsetInformacionProductoCarrito = mySql.ActualizarCantidadProductoCarrito(idProductoCarrito, cantidad, tipo);
    totalCarrito: getsetTotalesCarrito = mySql.ObtenerTotalesCarritoUsuario([])

    return jsonify({"resultado": json.dumps(res.__dict__), "total": json.dumps(totalCarrito.__dict__)})


@app.route('/EliminarProductoDelCarrito/', methods=['POST', 'GET'])
def EliminarProductoDelCarrito():
    idProductoCarrito = request.form['idProductoCarrito']

    mySql = MySQL()

    res = mySql.EliminarProductoCarrito(idProductoCarrito)

    return jsonify({"resultado": res})


@app.route('/ValidarExistenciaProducto/', methods=['POST', 'GET'])
def ValidarExistenciaProducto():
    codigoBarras = request.form['codigoBarras']

    mySql = MySQL()

    res = mySql.ObtenerExistenciaTotalProducto(codigoBarras)

    return jsonify({"resultado": res})


#
# if __name__ == '__main__':
#     print(__name__)
#     app.run()

@app.route('/productosVentaHistorial/', methods=['POST', 'GET'])
def productosVentaHistorial():
    idVentaEncriptado = request.args['idVentaEncriptado']
    idVenta: str = idVentaEncriptado;

    mySql = MySQL()

    productosVenta = mySql.ObtenerProductosVenta(idVenta);
    totalesVenta: getsetTotalesCarrito = mySql.ObtenerTotalesVenta(idVenta);
    totalesVenta.fuentePequena = True;
    detalles: getsetObjetoDetallesVentaHistorial = getsetObjetoDetallesVentaHistorial(productosVenta, totalesVenta,
                                                                                      mySql.ObtenerVenta(
                                                                                          idVenta).estatusVenta);

    return render_template('productosVentaHistorial.html', detalles=detalles, totalesVenta=totalesVenta)


@app.route('/AgregarProductoFavorito/', methods=['POST', 'GET'])
def AgregarProductoFavorito():
    idUsuario = request.form['idUsuario']
    idProducto = request.form['idProducto']
    mySql = MySQL()
    res = mySql.AgregarProductoFavorito(idProducto, idUsuario)

    return jsonify({"resultado": res[0], "mensaje": res[1]})


@app.route('/ValidarComentario/', methods=['POST', 'GET'])
def ValidarComentario():
    res = -3
    comentario = request.form['comentario']
    if comentario is None or comentario == "":
        res = -2
    else:
        res = 1

    return jsonify({"resultado": res})


@app.route('/ValidarTema/', methods=['POST', 'GET'])
def ValidarTema():
    res = -3
    minimo = 8
    maximo = 50
    tema = request.form['tema']
    if tema is None:
        res = -2
    else:
        if tema == "":
            res = -2
        else:
            if len(tema) < 8:
                res = -4
            else:
                if len(tema) > 50:
                    res = -5
                else:
                    res = 1

    return jsonify({"resultado": res})


@app.route('/ModificarComentarioUsuario/', methods=['POST', 'GET'])
def ModificarComentarioUsuario():
    res = -1
    idcomentario = request.form['idcomentario']
    tema = request.form['tema']
    comentario = request.form['comentario']

    if tema is None:
        res = -2
    else:
        if tema == "":
            res = -2
        else:
            if len(tema) < 8:
                res = -4
            else:
                if len(tema) > 50:
                    res = -5
                else:
                    if comentario is not None:
                        if comentario == "":
                            res = -6
                        else:
                            mysql = MySQL()
                            mysql.ModificarComentario(idcomentario, tema, comentario)
                            res = 1
                    else:
                        res = -6

    return jsonify({"resultado": res})


@app.route('/AgregarComentario/', methods=['POST', 'GET'])
def AgregarComentario():
    res = -1
    idcom = -1
    idUsuario = request.form['idUsuario']
    tema = request.form['tema']
    comentario = request.form['comentario']

    if tema is None:
        res = -2
    else:
        if tema == "":
            res = -2
        else:
            if len(tema) < 8:
                res = -4
            else:
                if len(tema) > 50:
                    res = -5
                else:
                    if comentario is not None:
                        if comentario == "":
                            res = -6
                        else:
                            mysql = MySQL()
                            idcom = mysql.AgregarComentarioUsuario(idUsuario, tema, comentario)
                            if idcom > 0:
                                res = 1
                    else:
                        res = -6

    return jsonify({"resultado": res, "idcomentario": idcom})


@app.route('/ObtenerInformacionComentario/', methods=['POST', 'GET'])
def ObtenerInformacionComentario():
    res = -1
    idcomentario = request.form['idcomentario']
    mysql = MySQL()
    comentarios = mysql.ObtenerComentarioUsuario("-1", idcomentario, True)
    res = 1
    return jsonify({"resultado": res, "comentariotema": comentarios[0].tema, "comentario": comentarios[0].comentario})


@app.route('/EliminarComentarioUsuario/', methods=['POST', 'GET'])
def EliminarComentarioUsuario():
    res = -1
    idcomentario = request.form['idcomentario']
    mysql = MySQL()
    mysql.EliminarComentarioUsuario(idcomentario, 1)
    res = 1
    return jsonify({"resultado": res})

def PagoAprobado(external_reference, payment_id="", status="",  comerciante_order_id="",  id =""):
    mysql = MySQL()
    idVenta = external_reference;
    venta = mysql.ObtenerVenta(idVenta);
    usuarioRegistrado = mysql.ObtenerUsuarioPorID(venta.idUsuario);
    pagada = False;
    tipoPago = venta.idTipoPago;
    enProceso = False;
    rechazada = False;
    enviarADomicilio = False;
    urlCodigoBarras = "";
