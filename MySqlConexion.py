import mysql.connector

from Programacion.Funcionalidad.Encriptacion import Encriptacion
from Programacion.getset import getsetUsuarioRegistrado
from Programacion.getset.getsetBadgeFlotante import getsetBadgeFlotante
from Programacion.getset.getsetCategoria import getsetCategoria
from Programacion.getset.getsetComentario import getsetComentario
from Programacion.getset.getsetConfiguracionWeb import getsetConfiguracionWeb
from Programacion.getset.getsetDepartamento import getsetDepartamento
from Programacion.getset.getsetDepartamentoLinea import getsetDepartamentoLinea
from Programacion.getset.getsetDepartamentoMarca import getsetDepartamentoMarca
from Programacion.getset.getsetDireccion import getsetDireccion
from Programacion.getset.getsetFiltros import getsetFiltros
from Programacion.getset.getsetInformacionProductoCarrito import getsetInformacionProductoCarrito
from Programacion.getset.getsetPreguntaAyuda import getsetPreguntaAyuda
from Programacion.getset.getsetProducto import getsetProducto
from Programacion.getset.getsetProductoFavorito import getsetProductoFavorito
from Programacion.getset.getsetProductoCarrito import getsetProductoCarrito
from Programacion.getset.getsetProductoPromocionPorCategoria import getsetProductoPromocionPorCategoria
from Programacion.getset.getsetProductoVenta import getsetProductoVenta
from Programacion.getset.getsetRespuestaAyuda import getsetRespuestaAyuda
from Programacion.getset.getsetRespuestaComentario import getsetRespuestaComentario
from Programacion.getset.getsetTemaAyuda import getsetTemaAyuda
from Programacion.getset.getsetUsuarioRegistrado import getsetUsuarioRegistrado
from Programacion.getset.getsetSugerenciaBusqueda import getsetSugerenciaBusqueda
from Programacion.getset.getsetTotalesCarrito import getsetTotalesCarrito
from Programacion.getset.getsetVenta import getsetVenta
from Programacion.getset.getsetTotalesCarrito import getsetTotalesCarrito


class MySQL:

    def __init__(self, host="bodegavalleverde.ddns.net", user="usuario1", pws="cotija20", bd="valleverdeecommerce"):
        self.HOST = host
        self.USER = user
        self.PASSWORD = pws
        self.DATABASE = bd
        self.CONNECTION = None
        # self.MYSQL_CURSOR = None

    def conectar_mysql(self, imprimir=False):
        conecto = False
        try:
            self.CONNECTION = mysql.connector.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                database=self.DATABASE,
                port=1600)
            conecto = True
        except Exception as error:
            conecto = False
            print("ERROR: ", error)
        return conecto

    def desconectar_mysql(self):
        if self.CONNECTION is not None:
            self.CONNECTION.close()
            self.CONNECTION = None
            # self.MYSQL_CURSOR = None

    def consulta_sql(self, sql, lectura=False, imprimir=False):
        # tieneRegistro = False;
        row = None
        resultados = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor(buffered=True)

            CURSOR.execute(sql)
            if lectura:
                for row in CURSOR:
                    resultados.append(row);
                    if imprimir:
                        print(row)
                '''row = CURSOR.fetchone()
                while row is not None:
                    #tieneRegistro = True;
                    print(row)
                    row = CURSOR.fetchone()
                '''
        except mysql.connector.errors.ProgrammingError as e:
            print("Error en la consulta ", e)
        except Exception as error:
            print("ERROR: ", error)

        self.CONNECTION.commit()
        CURSOR.close()
        self.desconectar_mysql()
        return resultados

    def ObtenerCategoria(self, tipo=-1, lectura=True, imprimir=True):
        row = None;
        resultados = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [tipo]
            CURSOR.callproc('ObtenerCategoria', args)
            if lectura:
                # for row in CURSOR.stored_results():
                #     resultados.append(row.fetchall())
                #     if imprimir:
                #         print(row)
                #         print(row.fetchall())
                for row in CURSOR.stored_results():
                    items = row.fetchall()
                    for item in items:
                        resultados.append(
                            getsetCategoria(item[0], item[1], item[2], item[2]))

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerCategoria: ", e)
        except Exception as error:
            print("ERROR ObtenerCategoria: ", error)

        CURSOR.close()
        self.desconectar_mysql()
        return resultados

    def ObtenerProductosCarouselPorCategoria(self, tipoCat, idProducto="-1", idLinea="-1", idMarca="-1",
                                             idFabricante="-1", idSubLinea="-1"):

        from Programacion.Funcionalidad.Utileria import Utileria
        obu = Utileria()
        titulo = ""
        match tipoCat:
            case 1:
                titulo = "En ofertas"
            case 2:
                titulo = "Destacados"
            case 3:
                titulo = "Relacionados"
            case 4:
                titulo = "Nuevos"

            # donde tipo es:
            # 1: ofertas toma en cuenta  el idmarca,fabricante ,linea y sublinea si se le manda,si no solo saca los que el precio promocion sea dif del precio normal
            # 2: mas vendidos/destacados  toma en cuenta el idmarca,fabricante , linea y sublinea si se le manda,si no solo filtra por CantidadVendidaActual desc
            # 3: relacionados toma en cuenta el idproducto y el idmarca,fabricante ,linea y sublinea si se le manda,si no se manda idproducto solo busca relaciones con las bandesras idLinea,marca,etc
            # 4: Ultimos agregados toma en cuenta el idmarca,fabricante ,linea,y sublinea  si se le manda,si no solo regresa los productos con fecha de alta mas reciente (FechaAlta desc)

        productos = []
        row = None
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [tipoCat, idProducto, idLinea, idMarca, idFabricante, idSubLinea]
            CURSOR.callproc('ObtenerProductosCarouselPorCategoria', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    interaccionConUsuario = item[5] > 0
                    imagenes = self.ObtenerImagenesProducto(item[0])
                    productos.append(getsetProducto(item[0], item[1], item[2], item[3], imagenes, False, 5, obu.RedondeoDouble(str(item[4])),
                                                    obu.RedondeoDouble(str(item[5])), obu.RedondeoDouble(str(5000)),
                                                    True, titulo, item[6], item[7], interaccionConUsuario))
            # CURSOR.close()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerProductosCarouselPorCategoria: ", e)
        except Exception as error:
            print("ERROR ObtenerProductosCarouselPorCategoria: ", error)

        self.desconectar_mysql()

        return productos

    def ObtenerImagenesProducto(self, idProducto):
        rutasImagenes = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idProducto]
            CURSOR.callproc('ObtenerImagenesProducto', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    rutasImagenes.append(item[0])

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerProductosCarouselPorCategoria: ", e)
        except Exception as error:
            print("ERROR: ", error)

        return rutasImagenes

    def ObtenerProducto(self, idProducto):
        producto = None
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idProducto]
            CURSOR.callproc('ObtenerProducto', args)

            for row in CURSOR.stored_results():

                interaccionConUsuario = False;
                items = row.fetchall()
                imagenes = self.ObtenerImagenesProducto(idProducto)
                for item in items:
                    if (item[4] > 0):
                        interaccionConUsuario = True

                    producto = getsetProducto(item[0], item[1], item[2], item[3],
                                              imagenes, False, 5, item[4]
                                              , item[5], 5000, True, "", item[6], item[7],
                                              interaccionConUsuario)
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return producto

    def ObtenerUsuarioPorToken(self, token):
        usuario:getsetUsuarioRegistrado = None;
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [token]
            CURSOR.callproc('ObtenerUsuarioPorToken', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    id = item[0]
                    direcciones = self.ObtenerDireccionUsuario(id);
                    usuario = getsetUsuarioRegistrado(id, item[1], item[2], item[3], item[4],
                                                      item[5], item[6], item[7], item[8], token, direcciones,
                                                      item[9], item[10], item[11], )
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return usuario;

    def ObtenerDireccionUsuario(self, idUsuario, idDireccion="-1"):
        direcciones = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idUsuario, idDireccion]
            CURSOR.callproc('ObtenerDireccionUsuario', args)

            for row in CURSOR.stored_results():

                items = row.fetchall()
                for item in items:
                    direcciones.append(getsetDireccion(item[0], item[1], item[2], item[3], item[4], item[5],
                                                       item[6], item[7], item[8], item[9],
                                                       item[10], item[11], item[12], item[13]))
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return direcciones

    def ObtenerProductosDePromocionPorCategoria(self, tipoCategoria=-1, numeroPagina=-1, numeroProductosPorPagina=-1):
        productosPromocion = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [tipoCategoria, numeroPagina, numeroProductosPorPagina]
            CURSOR.callproc('ObtenerProductosDePromocionPorCategoria', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    interaccionConUsuario = item[15] > 0
                    imagenes = self.ObtenerImagenesProducto(item[0])
                    productosPromocion.append(getsetProductoPromocionPorCategoria(item[0], item[1], item[2],
                                                                                  item[3], item[4], item[5], item[6],
                                                                                  item[7], item[8], item[9], item[10]
                                                                                  , item[11], item[12], item[13],
                                                                                  item[14], imagenes, item[15],
                                                                                  item[16], 5, False, 0, item[17],
                                                                                  interaccionConUsuario))

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return productosPromocion

    def ObtenerNumeroPaginasProductosDePromocionPorCategoria(self, tipoCategoria=-1, numeroProductosPorPagina="10"):
        productosPromocion = 0
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [tipoCategoria, numeroProductosPorPagina]
            CURSOR.callproc('ObtenerNumeroPaginasProductosDePromocionPorCategoria', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    productosPromocion = item[0]

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return productosPromocion

    def ObtenerTemasAyuda(self):
        temas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = []
            CURSOR.callproc('ObtenerTemasAyuda', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    idTema = item[0]
                    temas.append(getsetTemaAyuda(idTema, item[1], self.ObtenerPreguntasAyuda(idTema)))

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return temas

    def ObtenerPreguntasAyuda(self, idTema):
        preguntas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idTema]
            CURSOR.callproc('ObtenerPreguntasAyuda', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    idPregunta = item[0]
                    preguntas.append(
                        getsetPreguntaAyuda(idPregunta, idTema, item[1], self.ObtenerRespuestasAyuda(idPregunta)))

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return preguntas

    def ObtenerRespuestasAyuda(self, idPregunta):
        respuestas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idPregunta]
            CURSOR.callproc('ObtenerRespuestasAyuda', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    respuestas.append(getsetRespuestaAyuda(item[0], idPregunta, item[1]))

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return respuestas

    def ObtenerProductosCarritoUsuario(self, IDUsuarioRegistrado):
        res = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [IDUsuarioRegistrado]
            CURSOR.callproc('ObtenerProductosCarritoUsuario', args)

            ind = 0
            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    imagenes = self.ObtenerImagenesProducto(item[1])
                    res.append(getsetProductoCarrito(ind, item[0], item[1], item[2], item[3], item[4], item[5], item[6],
                                                     item[7], item[8], item[9], item[10], item[11], item[12], item[13],
                                                     item[14], imagenes, item[15], item[16], item[17], item[18]))
                    ind+=1
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerProductosCarritoUsuario: ", e)
        except Exception as error:
            print("ERROR ObtenerProductosCarritoUsuario: ", error)
        return res

    # def ObtenerTotalesCarritoUsuario(self, IDUsuarioRegistrado):
    #     res = getsetTotalesCarrito()
    #     if self.CONNECTION is None:
    #         self.conectar_mysql()
    #     try:
    #         CURSOR = self.CONNECTION.cursor()
    #         args = [IDUsuarioRegistrado]
    #         CURSOR.callproc('ObtenerTotalesCarritoUsuario', args)
    #
    #         for row in CURSOR.stored_results():
    #             items = row.fetchall()
    #             for item in items:
    #                 res = getsetTotalesCarrito(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
    #         CURSOR.close()
    #         self.desconectar_mysql()
    #
    #     except mysql.connector.errors.ProgrammingError as e:
    #         print("Error en el procedimiento ObtenerTotalesCarritoUsuario: ", e)
    #     except Exception as error:
    #         print("ERROR ObtenerTotalesCarritoUsuario: ", error)
    #     return res

    def ObtenerTotalesParaBadgeFlotantes(self, IDUsuarioRegistrado):
        res = getsetBadgeFlotante(0, 0, 0)
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [IDUsuarioRegistrado]
            CURSOR.callproc('ObtenerTotalesParaBadgeFlotantes', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = getsetBadgeFlotante(item[0], item[1], item[0] + item[1])
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerTotalesParaBadgeFlotantes: ", e)
        except Exception as error:
            print("ERROR ObtenerTotalesParaBadgeFlotantes: ", error)
        return res

    def ObtenerDepartamentos(self, tipo=-1, idDepartamento=-1):
        departamentos = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [tipo, idDepartamento]
            CURSOR.callproc('ObtenerDepartamentos', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    departamentos.append(getsetDepartamento(item[0], item[1], item[2], item[3],
                                                  self.ObtenerDepartamentoLinea(item[0]),
                                                  self.ObtenerDepartamentoMarca(item[0]),))

            # CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerDepartamentos: ", e)
        except Exception as error:
            print("ERROR ObtenerDepartamentos: ", error)

        return departamentos

    def ObtenerDepartamentoLinea(self, idDepartamento, tipo=1):

        departamentosLineas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idDepartamento, tipo]
            CURSOR.callproc('ObtenerDepartamentoLinea', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    departamentosLineas.append(getsetDepartamentoLinea(item[0], item[1], item[2], item[3], item[4], 2, Encriptacion.Encrypt("2")))
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerDepartamentos: ", e)
        except Exception as error:
            print("ERROR ObtenerDepartamentos: ", error)

        return departamentosLineas

    def ObtenerDepartamentoMarca(self, idDepartamento, tipo=1):

        departamentoMarcas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idDepartamento, tipo]
            CURSOR.callproc('ObtenerDepartamentoMarca', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    departamentoMarcas.append(getsetDepartamentoMarca(item[0], item[1], item[2], item[3], item[4], 1, Encriptacion.Encrypt("1")))
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerDepartamentoMarca: ", e)
        except Exception as error:
            print("ERROR ObtenerDepartamentoMarca: ", error)

        return departamentoMarcas

    def ObtenerComentarioUsuario(self, idUsuario, idComentario="-1", activo=True):
        comentarios = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idUsuario, idComentario, activo, None , None]
            CURSOR.callproc('ObtenerComentarioUsuario', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                pos = 0
                for item in items:
                    idComen = item[0]
                    comentarios.append(
                        getsetComentario(pos, idComen, item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                                         item[8], self.ObtenerRespuestaCometario(idComen)))
                    pos = pos + 1

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return comentarios

    def ObtenerRespuestaCometario(self, idComentario):
        respuestas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idComentario]
            CURSOR.callproc('ObtenerRespuestaCometario', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                pos = 0
                for item in items:
                    respuestas.append(getsetRespuestaComentario(item[0], item[1], item[2], item[3], item[4]))
                    pos = pos + 1

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return respuestas

    def ExisteUsuario(self, usuario, idUsuario="-1"):
        res = -3;
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [usuario, idUsuario]
            CURSOR.callproc('ExisteUsuario', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = item[0]

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return res

    def ValidarDatosInicioSesion(self, usuario, contrasena):
        res = -3;
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [usuario, contrasena]
            CURSOR.callproc('ValidarDatosInicioSesion', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = item[0]

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return res

    def AgregarSesionUsuario(self, usuario):
        res = ["-3","",""];
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [usuario]
            CURSOR.callproc('AgregarSesionUsuario', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = [item[0], item[1].decode('utf-8'), item[2].strftime('%Y-%m-%d')]

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return res

    def ObtenerFiltros(self, tipo):
        res = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [tipo]
            CURSOR.callproc('ObtenerFiltros', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res.append(getsetFiltros(item[0],item[1],item[2],item[3],item[4]))

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerFiltros: ", e)
        except Exception as error:
            print("ERROR ObtenerFiltros: ", error)

        return res

    def ObtenerProductos(self, numerPagina, productosPagina, idMarca , idLinea, idFabricante, idDepartamento,
                         busqueda, idSubLinea):
        res = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [numerPagina, productosPagina, idMarca , idLinea,idSubLinea, idFabricante, idDepartamento,
                         busqueda]
            CURSOR.callproc('ObtenerProductos', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    interaccionConUsuario = False
                    if (item[4] > 0):
                        interaccionConUsuario = True
                    imagenes = self.ObtenerImagenesProducto(item[0])
                    res.append(getsetProducto(item[0], item[1], item[2], item[3],
                                              imagenes, False, 5, item[4]
                                              , item[5], 5000, True, "", item[6], item[7],
                                              interaccionConUsuario))
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerProductos:", e)
        except Exception as error:
            print("ERROR ObtenerProductos: ", error)

        return res

    def ObtenerNumeroPaginasProductos(self, productosPagina, idMarca, idLinea, idFabricante, idDepartamento, busqueda,
                                      idSubLinea):
        paginas = 0
        res = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [productosPagina, idMarca, idLinea,idSubLinea, idFabricante, idDepartamento, busqueda]
            CURSOR.callproc('ObtenerNumeroPaginasProductos', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    paginas = int(item[0])
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ObtenerNumeroPaginasProductos:", e)
        except Exception as error:
            print("ERROR ObtenerNumeroPaginasProductos: ", error)

        return paginas

    # def ObtenerTotalesCarritoUsuario(self, idUsuario):
    #     totalCarrito = getsetTotalesCarrito();
    #     if self.CONNECTION is None:
    #         self.conectar_mysql()
    #     try:
    #         CURSOR = self.CONNECTION.cursor()
    #         args = [idUsuario]
    #         CURSOR.callproc('ObtenerTotalesCarritoUsuario', args)
    #
    #         for row in CURSOR.stored_results():
    #             items = row.fetchall()
    #             for item in items:
    #                 totalCarrito = getsetTotalesCarrito(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
    #
    #         self.CONNECTION.commit()
    #         CURSOR.close()
    #         self.desconectar_mysql()
    #
    #     except mysql.connector.errors.ProgrammingError as e:
    #         print("Error en el procedimiento ", e)
    #     except Exception as error:
    #         print("ERROR: ", error)
    #
    #     return totalCarrito

    def ObtenerTotalesCarritoUsuario(self, productos):
        subtotal = float(0)
        for producto in productos:
            subtotal += float(producto.precioPromocion) * float(producto.cantidad)
        envio = float(0)
        comision = float(5)
        descuento = float(0)
        total = float(subtotal)
        totalCarrito = getsetTotalesCarrito(subtotal, envio, comision, descuento, total, False, 1)
        return totalCarrito

    def ObtenerConfiguracionWeb(self):
        configuracion: getsetConfiguracionWeb() = None;
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = []
            CURSOR.callproc('ObtenerConfiguracionWeb', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    configuracion = getsetConfiguracionWeb(item[0])

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return configuracion

    def ObtenerProductosFavoritos(self, idUsuario):
        productosFavoritos = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idUsuario]
            CURSOR.callproc('ObtenerProductosFavoritos', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                ind = 0
                for item in items:
                    interaccionConUsuario = False
                    if item[10]:
                        interaccionConUsuario = True

                    idProductoFavorito = item[0]
                    imagenes = self.ObtenerImagenesProducto(item[1])

                    productosFavoritos.append(
                        getsetProductoFavorito(ind, item[0], item[1], item[2], item[3], item[4], item[5], item[6],
                                               item[7], item[8], item[9], item[10], item[11], imagenes,
                                               idProductoFavorito,
                                               interaccionConUsuario))
                    ind = ind + 1

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return productosFavoritos

    def ObtenerVentasUsuario(self, idUsuario, filtrar=False, cancelada=False):
        ventas = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idUsuario, filtrar, cancelada]
            CURSOR.callproc('ObtenerVentasUsuario', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                ind = 0
                for item in items:
                    res = item[0]
                    ventas.append(getsetVenta(res,
                                              item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                                              item[8], item[9], item[10], res, item[11], item[12]))

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return ventas

    def EliminarSesionUsuario(self, token):

        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [token]
            CURSOR.callproc('EliminarSesionUsuario', args)

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

    def ObtenerSugerenciasBusqueda(self, busqueda):
        res =  {}
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [busqueda]
            CURSOR.callproc('ObtenerSugerenciasBusqueda', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                indice = 1
                for item in items:
                    res[indice] = { "idProducto" :str(item[0]),"codigoBarras" :str(item[1]),"nombre" :str(item[2])}
                    indice += 1

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return res

    def AgregarProductoCarritoUsuario(self, idUsuario, idProducto, cantidad):
        res = ["-2", "Error metodo"]
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idUsuario, idProducto, cantidad]
            CURSOR.callproc('AgregarProductoCarritoUsuario', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = [str(item[0]), str(item[1])]

            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento AgregarProductoCarritoUsuario: ", e)
        except Exception as error:
            print("ERROR AgregarProductoCarritoUsuario: ", error)

        return res

    def ActualizarCantidadProductoCarrito(self, idProductoCarrito, cantidad, tipo):
        res = getsetInformacionProductoCarrito("","","",0,0,0,0,0,0)
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idProductoCarrito, cantidad, tipo]
            CURSOR.callproc('ActualizarCantidadProductoCarrito', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = getsetInformacionProductoCarrito(item[0], item[1], item[2], item[3], item[4], item[5],
                                                           item[6], item[7],item[8])
            self.CONNECTION.commit()
            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ActualizarCantidadProductoCarrito: ", e)
        except Exception as error:
            print("ERROR ActualizarCantidadProductoCarrito: ", error)

        return res

    def EliminarProductoCarrito(self, idProductoCarrito):
        res = -1
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idProductoCarrito]
            CURSOR.callproc('EliminarProductoCarrito', args)
            self.CONNECTION.commit()

            res = 1

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento EliminarProductoCarrito: ", e)
        except Exception as error:
            print("ERROR EliminarProductoCarrito: ", error)

        return res

    def ObtenerExistenciaTotalProducto(self, codigoBarras):
        res = 400

        return res

    def ObtenerProductosVenta(self, idVenta):
        productos = []
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idVenta]
            CURSOR.callproc('ObtenerProductosVenta', args)

            for row in CURSOR.stored_results():
                items = row.fetchall()
                ind: int = 0
                for item in items:
                    productos.append(getsetProductoVenta(ind,item[0], item[1], item[2],
                                                                                  item[3], item[4], item[5], item[6],
                                                                                  item[7], item[8], item[9], item[10]
                                                                                  , item[11], item[12]))
                    ind = ind+1

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return productos

    def ObtenerTotalesVenta(self, idVenta):
        res = None
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idVenta]
            CURSOR.callproc('ObtenerTotalesVenta', args)
            self.CONNECTION.commit()

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = getsetTotalesCarrito(item[0],item[1],item[2],item[3],item[4],item[5],item[6])

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento EliminarProductoCarrito: ", e)
        except Exception as error:
            print("ERROR EliminarProductoCarrito: ", error)

        return res

    def ObtenerVenta(self, idVenta):
        res = None
        if self.CONNECTION is None:
            self.conectar_mysql()
        try:
            CURSOR = self.CONNECTION.cursor()
            args = [idVenta]
            CURSOR.callproc('ObtenerVenta', args)
            self.CONNECTION.commit()

            for row in CURSOR.stored_results():
                items = row.fetchall()
                for item in items:
                    res = getsetVenta(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[0],item[11],item[12])

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento EliminarProductoCarrito: ", e)
        except Exception as error:
            print("ERROR EliminarProductoCarrito: ", error)

        return res