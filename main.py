import json
import qrcode
from flask import Flask, render_template, Blueprint, request, jsonify
from flask_cors import CORS
from werkzeug.urls import url_encode

from MySqlConexion import MySQL
from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.Funcionalidad.MercadoPagoMetodos import MercadoPagoMetodos
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
from Programacion.getset.getsetObjetoProcesoCompra import getsetObjetoProcesoCompra
from Programacion.getset.getsetObjetoProducto import getsetObjetoProducto
from Programacion.getset.getsetObjetoProductos import getsetObjetoProductos
from Programacion.getset.getsetObjetoProductosFavoritos import getsetObjetoProductosFavoritos
from Programacion.getset.getsetObjetoPromociones import getsetObjetoPromociones
from Programacion.getset.getsetResultado import getsetResultado
from Programacion.getset.getsetTotalesCarrito import getsetTotalesCarrito
from Programacion.getset.getsetVenta import getsetVenta
from Programacion.getset.getsetObjetoPagoAprobado import getsetObjetoPagoAprobado

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
            totalCarrito = mySql.ObtenerTotalesCarritoUsuario(datosUsuario.IDUsuarioRegistrado)
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
    numeroPagina: int = int(request.args.get('numeroPagina', 1))

    if (productosPag == -2):
        productosPag = 10

    numeroCuadrosPagina = 5

    # if (_detectionService.Device.Type == Device.Mobile)
    #   numeroCuadrosPagina = 4;

    productosPromocion = mySql.ObtenerProductosDePromocionPorCategoria(2);

    productosPromocionIndividuales = mySql.ObtenerProductosDePromocionPorCategoria(-1, numeroPagina-1, productosPag);

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
    mySql = MySQL()

    listaCodigosTelefono = mySql.ObtenerCodigoTelefonoPais()

    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(False, "")
    # ----------------------------
    return render_template('registrar.html',informacionCabecera=informacionCabecera,
                           listaCodigosTelefono=listaCodigosTelefono)


@app.route('/producto', methods=['POST', 'GET'])
def producto(tipo=-1, busqueda="", idProducto=""):
    patch = request.endpoint.split("/")
    idProducto = request.args['idProducto'];
    mySql = MySQL();

    productosCarousel = mySql.ObtenerProductosCarouselPorCategoria(3, idProducto);
    productoSeleccionado = mySql.ObtenerProducto(idProducto);
    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, busqueda)
    # ----------------------------
    informacionCarousel = getsetInformacionCarousel(None, productosCarousel, datosUsuario);
    informacion = getsetObjetoProducto(None, busqueda, productosCarousel, productoSeleccionado, None, datosUsuario,
                                       informacionCabecera, informacionCarousel)
    patch.append(productoSeleccionado.nombreProducto)
    return render_template('Producto.html', ObjetoProducto=informacion, patch=patch, Usuario=datosUsuario)


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
        productosCarousel = mysql.ObtenerProductosCarouselPorCategoria(2)
        objCarritoUsuario = getsetObjetoCarritoUsuario(None, "", productosCarousel, productosCarritos, datosUsuario, informacionCabecera.totalCarrito,
                                                       False, None, mysql.ObtenerConfiguracionWeb())
        productosFavoritos = mysql.ObtenerProductosFavoritos(datosUsuario.IDUsuarioRegistrado)
        objFavoritos = getsetObjetoProductosFavoritos(productosFavoritos, datosUsuario)
        objetoCarrito = getsetObjetoCarrito(objCarritoUsuario, objFavoritos, Favoritos)


    return render_template('carritoUsuario.html', objetoCarrito=objetoCarrito, informacionCabecera=informacionCabecera, EsParaFavoritos=False)


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
                                                       informacionCabecera.totalCarrito,
                                                       False, None, mysql.ObtenerConfiguracionWeb())
        productosFavoritos = mysql.ObtenerProductosFavoritos(datosUsuario.IDUsuarioRegistrado)
        objFavoritos = getsetObjetoProductosFavoritos(productosFavoritos, datosUsuario)
        objetoCarrito = getsetObjetoCarrito(objCarritoUsuario, objFavoritos, True)
    # ----------------------------
    return render_template('carritoUsuario.html', EsParaFavoritos=True, informacionCabecera=informacionCabecera,
                           objetoCarrito=objetoCarrito)


@app.route('/procesoCompra')
def procesoCompra():
    informacionCabecera = LlenarCabecera(False,'',False)

    usuarioActual = Utileria().ObtenerUsuarioDeLaSesionActual(request)

    mysql = MySQL()

    productosCarrito = mysql.ObtenerProductosCarritoUsuario(usuarioActual.IDUsuarioRegistrado);
    tipoPagos = mysql.ObtenerTipoPagos("-1");
    paqueteriaHabilitada = False;
    envioADomicilioPorDefecto = False;
    totalesCarrito: getsetTotalesCarrito = mysql.ObtenerTotalesCarritoUsuario(usuarioActual.IDUsuarioRegistrado);

    objetoVenta:getsetObjetoProcesoCompra = getsetObjetoProcesoCompra(usuarioActual.IDUsuarioRegistrado,tipoPagos,None,productosCarrito,paqueteriaHabilitada, envioADomicilioPorDefecto, mysql.ObtenerTipoPagoCarrito(usuarioActual.IDUsuarioRegistrado),totalesCarrito);


    return render_template('procesoCompra.html',objetoVenta=objetoVenta,informacionCabecera=informacionCabecera)


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
    mySql = MySQL()
    # cabecera-----------------------------
    informacionCabecera = LlenarCabecera(True, "")
    # ----------------------------

    datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
    listaPaises = mySql.ObtenerPaisesConCodigosIso()
    pais = next((obj for obj in listaPaises if obj.nombrePais == 'Mexico'), listaPaises[0])
    listaEstados = mySql.ObtenerEstadosPorPais(pais.nombrePais, pais.iso3)
    listaCiudades = mySql.ObtenerCiudadesPorEstadoPais(pais.nombrePais, listaEstados[0].nombreEstado)
    listaCodigosTelefono = mySql.ObtenerCodigoTelefonoPais()
    listaColonias = mySql.ObtenerColoniaPorCodigoPostal("")
    identificacion = None

    informacionUsuario = getsetObjetoPerfilUsuario(datosUsuario, "","","", listaPaises, listaEstados, listaCiudades,
                                                   listaColonias, listaCodigosTelefono, identificacion)
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

    return jsonify({"res": "Sesion cerrada"})\

@app.route('/validarBusqueda/', methods=['POST', 'GET'])
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

    usuario = Utileria().ObtenerUsuarioDeLaSesionActual(request);

    mySql = MySQL()

    if(float(cantidad)>0):
        res: getsetInformacionProductoCarrito = mySql.ActualizarCantidadProductoCarrito(idProductoCarrito, cantidad, tipo);
        totalCarrito: getsetTotalesCarrito = mySql.ObtenerTotalesCarritoUsuario(usuario.IDUsuarioRegistrado)
        return jsonify({"resultado": json.dumps(res.__dict__), "total": json.dumps(totalCarrito.__dict__)})
    else:
        res = mySql.EliminarProductoCarrito(idProductoCarrito);
        totalCarrito: getsetTotalesCarrito = mySql.ObtenerTotalesCarritoUsuario(usuario.IDUsuarioRegistrado)
        return jsonify({"resultado": res, "total": json.dumps(totalCarrito.__dict__)})




    res: getsetInformacionProductoCarrito = mySql.ActualizarCantidadProductoCarrito(idProductoCarrito, cantidad, tipo);
    totalCarrito: getsetTotalesCarrito = mySql.ObtenerTotalesCarritoUsuario(idUsuario)

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

@app.route('/pagoAprobado/', methods=['POST', 'GET'])
def PagoAprobado():
    mysql = MySQL()

    external_reference = request.args.get('external_reference',-1);
    payment_id = request.args.get('payment_id',"");
    status = request.args.get('status',"");
    comerciante_order_id = request.args.get('comerciante_order_id',"");
    id = request.args.get('id',"");

    idVenta = external_reference;
    venta = mysql.ObtenerVenta(idVenta);
    usuarioRegistrado = Utileria().ObtenerUsuarioDeLaSesionActual(request);
    pagada = False;
    tipoPago = venta.idTipoPago;
    enProceso = False;
    rechazada = False;
    enviarADomicilio = False;
    urlCodigoBarras = 'static/wwwroot/Temp/QR_' + idVenta + '.png'
    codigoQR = qrcode.make(idVenta)
    codigoQR.save(urlCodigoBarras);

    if (tipoPago == 1):
        enProceso = False;
        enviarADomicilio = False;


        # Saving as an image file


    if (tipoPago == 2):
        #Verificar con mercadolibre que se haya pagado y marcarla pagada
        if (payment_id != "null" and payment_id != ""):
            #Programacion.Funcionalidad.MercadoPagoMetodos obm = new Programacion.Funcionalidad.MercadoPagoMetodos();
            #Payment pago = obm.ObtenerPago(payment_id);

            #if (pago.Status == "approved" and pago.StatusDetail == "accredited" and pago.TransactionAmount >= (decimal)venta.total):
            pagada = True;

            #enviarADomicilio = venta.enviarADomicilio;
            #urlCodigoBarras = new Programacion.Funcionalidad.Utileria().GenerarCodigoBarras(Environment, idVenta);
            #Marcar pagada
                #if (!venta.pagada):
                #    string[] res = obv.MarcarVentaPagada(idVenta, payment_id);

        else:
            #Si llego aqui de una venta de mercado pago pero sin payment_id probablemente usaron el boton volver al sitio
            pagada = False;
            enProceso = False;
            rechazada = True;

    objPagoAprobado = getsetObjetoPagoAprobado(venta, payment_id, tipoPago, pagada, enProceso, rechazada,
                             usuarioRegistrado, enviarADomicilio, urlCodigoBarras)

    informacionCabecera = LlenarCabecera("",True)

    return render_template('pagoAprobado.html',objPagoAprobado=objPagoAprobado,informacionCabecera=informacionCabecera)

@app.route('/ActualizarTipoEnvio/', methods=['POST', 'GET'])
def ActualizarTipoEnvio():
    valor = request.form['valor'];

    mysql = MySQL()

    usuario:getsetUsuarioRegistrado = Utileria().ObtnerUsuarioDeLaSesionActual(request);
    mysql.ActualizarTipoEnvioCarrito(usuario.IDUsuarioRegistrado,valor);

    return jsonify({"resultado": 1})

@app.route('/RetomarPago/', methods=['POST', 'GET'])
def RetomarPago():
    idVentaEncriptado = request.form['idVentaEncriptado'];

    mysql = MySQL()
    idVenta = idVentaEncriptado;

    venta:getsetVenta = mysql.ObtenerVenta(idVenta);

    if (venta != None and venta.idTipoPago == 2):
        idPreferencia = "";

        preferencia = MercadoPagoMetodos().CrearPreferencia(venta.idVenta, idVentaEncriptado);
        return jsonify( { "url" : preferencia['sandbox_init_point'], "estado" : 1, "mensaje" : "" });

    else:
        return jsonify({ "url" : "", "estado": -1,"mensaje" : "No se pudo generar el cargo" });


@app.route('/CrearVenta/', methods=['POST', 'GET'])
def CrearVenta():
    idUsuarioEncriptado = request.form['idUsuarioEncriptado'];

    mysql = MySQL()
    idVenta = idUsuarioEncriptado;

    idUsuario = idUsuarioEncriptado;

    res= mysql.ConvertirCarritoEnVentaUsuario(idUsuario);

    if (res[0]!=-1):
        venta = mysql.ObtenerVenta(res[0]);


        if (venta.idTipoPago == 1):
            #Pago en tienda
            url = "/pagoAprobado?external_reference=" + str(venta.idVentaEncriptada);

            return jsonify({"url": url, "estado": 1});

        else:
            if(venta.idTipoPago == 2 or venta.idTipoPago == 3 or venta.idTipoPago == 4):
                #Pago en MercadoPago u OpenPay

                preferencia = MercadoPagoMetodos().CrearPreferencia(venta.idVenta);

                if (preferencia != None):
                    return jsonify( { "url" : preferencia["sandbox_init_point"], "estado" : 1 });
                else:
                    return jsonify( { "url" : "", "estado" : -1 });


    else:
        return jsonify({"url": "", "estado": -1});



@app.route('/ActualizarTipoPagoCarrito/', methods=['POST', 'GET'])
def ActualizarTipoPagoCarrito():
    idTipoPago = request.form['idTipoPago'];

    mysql = MySQL()

    usuario = Utileria().ObtenerUsuarioDeLaSesionActual(request);

    mysql.ActualizarTipoPagoCarrito(usuario.IDUsuarioRegistrado, idTipoPago);

    return jsonify( {"actualizado" : 1});




@app.route('/ValidarNombre/', methods=['POST', 'GET'])
def ValidarNombre():
    nombre = request.form['nombre']
    res = Utileria().ValidarNombreApellidosUsuario(nombre)
    return jsonify({"resultado":res})


@app.route('/ValidarApellidos/', methods=['POST', 'GET'])
def ValidarApellidos():
    apellidos = request.form['apellidos']
    res = Utileria().ValidarNombreApellidosUsuario(apellidos)
    return jsonify({"resultado":res})

@app.route('/ValidarCorreo/', methods=['POST', 'GET'])
def ValidarCorreo():
    correo = request.form['correo']
    modificacion = request.form['modificacion']
    res = Utileria().ValidarCorreoUsuario(correo, modificacion, request)
    return jsonify({"resultado":res})

@app.route('/ValidarTelefono/', methods=['POST', 'GET'])
def ValidarTelefono():
    telefono = request.form['telefono']
    modificacion = request.form['modificacion']
    res = Utileria().ValidarTelefonoUsuario(telefono, modificacion, request)
    return jsonify({"resultado":res})

@app.route('/ValidarUsuario/', methods=['POST', 'GET'])
def ValidarUsuario():
    usuario = request.form['usuario']
    modificacion = bool(request.form['modificacion'])
    res = Utileria().ValidarUsuario(usuario, modificacion, request)
    return jsonify({"resultado":res})

@app.route('/ValidarContraseña/', methods=['POST', 'GET'])
def ValidarContraseña():
    contrasena = request.form['contraseña']
    res = Utileria().ValidarContraseñaUsuario(contrasena)
    return jsonify({"resultado":res})

@app.route('/ValidarContraseñaActual/', methods=['POST', 'GET'])
def ValidarContraseñaActual():
    contrasena = request.form['contraseña']
    res = Utileria().ValidarContraseñaActualUsuario(contrasena, request, MySQL())
    return jsonify({"resultado":res})

@app.route('/ValidarConfirmarContraseña/', methods=['POST', 'GET'])
def ValidarConfirmarContraseña():
    contrasena = request.form['contraseña']
    contrasenaValidad = request.form['contraseñaconfirmar']
    res = Utileria().ValidarConfirmarContraseñaUsuario(contrasena, contrasenaValidad)
    return jsonify({"resultado":res})

@app.route('/CrearCuenta/', methods=['POST', 'GET'])
def CrearCuenta():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    telefono = request.form['telefono']
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    contraseñaConf = request.form['contraseñaConf']
    codigoTelefono = request.form['codigoTelefono']

    mySql = MySQL()
    resB = None
    sesion = None
    try:
        resB = mySql.AgregarUsuario(nombre, apellido, correo, telefono, usuario, contraseña, contraseñaConf,
                                  codigoTelefono)
        sesion = mySql.AgregarSesionUsuario(usuario)

    except Exception as e:
        pass

    if resB == None:
        resB = ["-1", "Error Desconocido"]
    if sesion == None:
        sesion = ["-1", "Desconocido", "Desconocida"]

    return jsonify({ "resultadoC": resB[0], "resultadoM": resB[1], "token": sesion[1],
                     "fechaExpiracion": sesion[2] })

@app.route('/ObtenerDatosOriginalesUsuario/', methods=['POST', 'GET'])
def ObtenerDatosOriginalesUsuario():
    token = None
    idUsuarioRegistrado = "-1"
    nombre = ""
    apellido = ""
    telefono = ""
    usuario = ""
    contraseña = ""
    fechaRegistro = ""
    correo = ""
    codigo = ""
    activo = False
    Obusuario = Utileria().ObtenerUsuarioDeLaSesionActual(request=request)

    if Obusuario is not None:
        token = str(Obusuario.token)
        idUsuarioRegistrado = Obusuario.IDUsuarioRegistrado
        nombre = Obusuario.Nombre
        apellido = Obusuario.Apellido
        telefono = Obusuario.Telefono
        usuario = Obusuario.Usuario
        contraseña = Obusuario.Contraseña
        fechaRegistro = Obusuario.FechaRegistro
        correo = Obusuario.Correo
        activo = Obusuario.Activo
        codigo = Obusuario.idCodigoTelefono
    listaCodigosTelefono = MySQL().ObtenerCodigoTelefonoPais()
    telefonos = json.dumps([tel.__dict__ for tel in listaCodigosTelefono])
    return jsonify({"token":token, "IDUsuarioRegistrado": idUsuarioRegistrado, "nombre": nombre, "apellido": apellido,
                    "telefono": telefono, "usuario": usuario, "Contraseña": contraseña, "FechaRegistro": fechaRegistro,
                    "Activo": activo, "correo": correo, "codigo": codigo,
                    "codigos": telefonos})

@app.route('/GuardarDatosPersonales/', methods=['POST', 'GET'])
def GuardarDatosPersonales():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    telefono = request.form['telefono']
    codigoTelefono = request.form['codigoTelefono']
    modificacion = bool(request.form['modificacion'])
    res = -1
    mensaje = "Error metodo"
    resAux = -1

    util = Utileria()
    mySql =MySQL()

    resAux = util.ValidarNombreApellidosUsuario(nombre)
    if resAux == 1:
        resAux = util.ValidarNombreApellidosUsuario(apellidos)
        if resAux == 1:
            resAux = util.ValidarCorreoUsuario(correo, modificacion, request)
            if (resAux == 1):
                if not codigoTelefono == "":
                    resAux = util.ValidarTelefonoUsuario(telefono, modificacion, request)
                    if (resAux == 1):
                        datosUsuario = util.ObtenerUsuarioDeLaSesionActual(request)
                        if (datosUsuario is not None):
                            print(datosUsuario.IDUsuarioRegistrado, )
                            res = mySql.ModificarUsuario(datosUsuario.IDUsuarioRegistrado, nombre, apellidos, telefono, correo, codigoTelefono)
                            if (res == 1):
                                mensaje = "Exito al modificar datos personales"
                        else:
                            mensaje = "Sesion no valida"
                    else:
                         #  1 todo bien
                         # -1 caracteres invalidos
                         # -2 vacio
                         # -3 error metodo
                         # -4 telefono no disponible
                        match resAux:
                            case -1:
                                mensaje = "Caracteres invalidos en el telefono"
                            case - 2:
                                mensaje = "El telefono no puede quedar vacio"
                            case - 3:
                                mensaje = "Error al validar el telefono"
                            case - 4:
                                mensaje = "Telefono no disponible"

                else:
                    mensaje = "El codigo de telefono no puede quedar vacio"

            else:
                # 1 todo bien
                # -2 vacio
                # -3 error metodo
                # -4 correo no disponible
                match resAux:
                    case - 1:
                        mensaje = "Caracteres invalidos en el correo"

                    case - 2:
                        mensaje = "El correo no puede quedar vacio"

                    case - 3:
                        mensaje = "Error al validar el correo"

                    case - 4:
                        mensaje = "Correo no disponible"

        else:
                # 1 todo bien
                # -2 vacio
                # -3 error metodo
                match resAux:
                    case -1:
                        mensaje = "Caracteres invalidos en el apellido"
                    case -2:
                        mensaje = "El apellido no puede quedar vacio"
                    case -3:
                        mensaje = "Error al validar el apellido"
    else:
        # 1 todo bien
        # -2 vacio
        # -3 error metodo
        match resAux:
            case - 1:
                mensaje = "Caracteres invalidos en el nombre"
            case - 2:
                mensaje = "El nombre no puede quedar vacio"
            case - 3:
                mensaje = "Error al validar el nombre"

    return jsonify({"resultado": res, "mensaje": mensaje})

@app.route('/EliminarProductoDeFavoritos/', methods=['POST', 'GET'])
def EliminarProductoDeFavoritos():
    idProductoFavorito = request.form['idProductoFavorito']
    mySql = MySQL()

    res = mySql.EliminarProductoFavorito(idProductoFavorito)

    return jsonify({"resultado": res})

@app.route('/ConvertirProductoDeFavoritoACarrito/', methods=['POST', 'GET'])
def ConvertirProductoDeFavoritoACarrito():
    idProductoFavorito = request.form['idProductoFavorito']
    mySql = MySQL()

    res = mySql.ConvertirProductoFavoritoAProductoCarrito(idProductoFavorito)

    return jsonify({"resultado": res})

@app.route('/GuardarDatosCuentaC/', methods=['POST', 'GET'])
def GuardarDatosCuentaC():
    contraseñaActual = request.form['contraseñaActual']
    contraseñaNueva = request.form['contraseñaNueva']
    contraseñaNuevaConfirmar = request.form['contraseñaNuevaConfirmar']

    res = -1
    resAux = -1
    idUsuario = "-1"
    mensaje = "Error metodo"

    util = Utileria()
    mySql =MySQL()

    resAux = util.ValidarContraseñaActualUsuario(contraseñaActual, request, mySql)
    if resAux == 1:
        resAux = util.ValidarContraseñaUsuario(contraseñaNueva)
        if resAux == 1:
            resAux = util.ValidarConfirmarContraseñaUsuario(contraseñaNueva, contraseñaNuevaConfirmar)
            if (resAux == 1):
                if not contraseñaActual == contraseñaNueva:
                    datosUsuario = util.ObtenerUsuarioDeLaSesionActual(request)
                    if (datosUsuario is not None):
                        idUsuario = datosUsuario.IDUsuarioRegistrado
                    res = mySql.ModificarContrasenaUsuario(contraseñaNueva, idUsuario)
                    if (res == 1):
                        mensaje = "Exito al modificar contraseña";
                else:
                    mensaje = "La contraseña nueva no puede ser igual a la actual";
            else:
                 #  1 todo bien
                 # -1 caracteres invalidos
                 # -2 vacio
                 # -3 error metodo
                 # -4 telefono no disponible
                match resAux:
                    case -1:
                        mensaje = "La contraseñas no coinciden";
                    case -2:
                        mensaje = "Confrimar contraseña no pude quedar vacio";
                    case -3:
                        mensaje = "Error al validar contraseña nueva";
        else:
            #  1 todo bien
            # -1 caracteres invalidos
            # -2 vacio
            # -3 error metodo
            # -4 telefono no disponible
            match resAux:
                case -1:
                    mensaje = "La contraseña nueva es incorrecta";
                case -2:
                    mensaje = "La contraseña nueva no puede quedar vacia";
                case -3:
                    mensaje = "Error al validar contraseña nueva";
                case -4:
                    mensaje = "La contraseña nueva no puede ser menor a 8 caracteres";
                case -5:
                    mensaje = "La contraseña nueva no puede ser mayor a 25 caracteres";
                case -6:
                    mensaje = "La contraseña nueva debe contener letras(s)";
                case -7:
                    mensaje = "La contraseña nueva  debe contener numero(s)";
    else:
        #  1 todo bien
        # -1 caracteres invalidos
        # -2 vacio
        # -3 error metodo
        # -4 telefono no disponible
        match resAux:
            case -1:
                mensaje = "La contraseña actual es incorrecta";
            case -2:
                mensaje = "La contraseña actual no puede quedar vacia";
            case -3:
                mensaje = "Error al validar contraseña actual";
            case -4:
                mensaje = "La contraseña actual no puede ser menor a 8 caracteres";
            case -5:
                mensaje = "La contraseña actual no puede ser mayor a 25 caracteres";

    return jsonify({"resultado": res, "mensaje":mensaje})

@app.route('/GuardarDatosCuentaU/', methods=['POST', 'GET'])
def GuardarDatosCuentaU():
    usuario = request.form['usuario']
    res = -1
    resAux = -1
    idUsuario = "-1"
    mensaje = "Error metodo"

    util = Utileria()
    mySql =MySQL()

    resAux = util.ValidarUsuario(usuario, True, request)
    if (resAux == 1):
        Obusuario = util.ObtenerUsuarioDeLaSesionActual(request)
        if (Obusuario is not None):
            idUsuario = Obusuario.IDUsuarioRegistrado
            print(idUsuario, usuario)
        res = mySql.ModificarCampoUsuario(usuario, idUsuario)
        print(res)
        if (res == 1):
            mensaje = "Exito al modificar usuario"
    else:
        match resAux:
            case -1:
                mensaje = "Caracteres invalidos en el usuario"
            case -2:
                mensaje = "El usuario no puede quedar vacio"
            case -3:
                mensaje = "Error al validar el usuario"
            case -4:
                mensaje = "Usuario no puede ser menor a 8 caracteres"
            case -5:
                mensaje = "Usuario no puede ser mayor a 20 caracteres"
            case -6:
                mensaje = "Usuario no disponible"

    return jsonify({"resultado": res, "mensaje": mensaje})


@app.route('/ObtenerDatosDireccionUsuario/', methods=['POST', 'GET'])
def ObtenerDatosDireccionUsuario():
    usuario = request.form['usuario']
    idDir = request.form['idDir']

    mySql = MySQL()

    listapaises = []
    listaestados = []
    listaciudades = []
    listacolonias = []

    listaDirecciones = mySql.ObtenerDireccionUsuario(usuario, idDir)
    d = None
    drop = -1

    if len(listaDirecciones) > 0:
        d = listaDirecciones[0]
        listapaises = mySql.ObtenerPaisesConCodigosIso()
        listaestados = mySql.ObtenerEstadosPorPais(d.pais, d.iso3Pais)
        listaciudades = mySql.ObtenerCiudadesPorEstadoPais(d.pais, d.estado)
        listacolonias = mySql.ObtenerColoniaPorCodigoPostal(d.codigoPostal)
        drop = 1

    return jsonify({"direccion": d, "paises": listapaises, "estados": listaestados, "ciudades": listaciudades,
                    "colonias": listacolonias, "drop": drop})

@app.route('/ObtenerEstadosPais/', methods=['POST', 'GET'])
def ObtenerEstadosPais():
    pais = request.form['pais']
    iso3 = request.form['iso3']

    mySql = MySQL()
    listaestados = mySql.ObtenerEstadosPorPais(pais, iso3)
    estados = json.dumps([estado.__dict__ for estado in listaestados])

    return jsonify({"estados": json.loads(estados)})

@app.route('/ObtenerCiudadesEstadoPais/', methods=['POST', 'GET'])
def ObtenerCiudadesEstadoPais():
    pais = request.form['pais']
    estado = request.form['estado']

    mySql = MySQL()
    listaCiudades =  mySql.ObtenerCiudadesPorEstadoPais(pais, estado)
    ciudades = json.dumps([ciudad.__dict__ for ciudad in listaCiudades])

    return jsonify({"ciudades": json.loads(ciudades)})


@app.route('/ObtenerColoniaPorCodigoPostal/', methods=['POST', 'GET'])
def ObtenerColoniaPorCodigoPostal():
    codigo = request.form['codigo']

    listacolonias = []
    mostraDrop = -1
    entro = False

    if (codigo is not None):
        if len(codigo) > 3:
            listacolonias = MySQL().ObtenerColoniaPorCodigoPostal(codigo)
            entro = True
        if (len(listacolonias) > 0):
            mostraDrop = 1

    colonias = json.dumps([col.__dict__ for col in listacolonias])

    return jsonify({"colonias": json.loads(colonias), "colonia": "", "codigod": "", "drop": mostraDrop,
                    "entro": entro})

@app.route('/GuardarDireccion/', methods=['POST', 'GET'])
def GuardarDireccion():
    idDir = request.form['idDir']
    ciudad= request.form['ciudad']
    colonia= request.form['colonia']
    calle= request.form['calle']
    nexterior= request.form['nexterior']
    ninterior= request.form['ninterior']
    destinatario= request.form['destinatario']
    isoPais= request.form['isoPais']
    pais= request.form['pais']
    estado= request.form['estado']
    codigoEstado= request.form['codigoEstado']
    codigoPostal = request.form['codigoPostal']

    mySql = MySQL()
    res = -1
    resAux = 0
    mensaje = "Error metodo"

    if idDir != "-1":
        mySql.ModificarDireccionUsuario(idDir, ciudad, colonia, calle, nexterior, ninterior, destinatario, isoPais, pais,
                                  estado, codigoEstado, codigoPostal)
        res = 1
        mensaje = "Exito al modificar"
    else:
        datosUsuario = Utileria().ObtenerUsuarioDeLaSesionActual(request)
        id = mySql.AgregarDireccionUsuario(datosUsuario.IDUsuarioRegistrado, ciudad, colonia, calle, nexterior, ninterior,
                                         destinatario, isoPais, pais, estado, codigoEstado, codigoPostal)
        if (id > 0):
            res = 1
            mensaje = "Exito al agregar direccion"

    return jsonify({"resultado": res, "mensaje": mensaje})


@app.route('/ObtenerEstadosPaisCiudadDefecto/', methods=['POST', 'GET'])
def ObtenerEstadosPaisCiudadDefecto():
    mySql = MySQL()
    listaPaises = mySql.ObtenerPaisesConCodigosIso()
    listaestados = mySql.ObtenerEstadosPorPais("Mexico", "MEX")
    listaciudades = mySql.ObtenerCiudadesPorEstadoPais("Mexico", listaestados[0].nombreEstado)

    paises = json.dumps([pais.__dict__ for pais in listaPaises])
    estados = json.dumps([estado.__dict__ for estado in listaestados])
    ciudades = json.dumps([ciudad.__dict__ for ciudad in listaciudades])

    return jsonify({"paises": json.loads(paises), "estados": json.loads(estados), "ciudades": json.loads(ciudades),
                    "pais": "Mexico", "iso": "MEX", "estado": listaestados[0].nombreEstado})

