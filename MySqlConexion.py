import mysql.connector

from Programacion.getset import getsetUsuarioRegistrado
from Programacion.getset.getsetProducto import getsetProducto


class MySQL:

    def __init__(self, host="192.168.0.106", user="usuario1", pws="cotija20", bd="valleverdeecommerce"):
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
                database=self.DATABASE)
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
                for row in CURSOR.stored_results():
                    resultados.append(row.fetchall())
                    if imprimir:
                        print(row)
                        print(row.fetchall())

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        CURSOR.close()
        self.desconectar_mysql()
        return resultados

    def ObtenerProductosCarouselPorCategoria(self, tipoCat, idProducto="-1", idLinea="-1", idMarca="-1",
                                             idFabricante="-1", idSubLinea="-1"):
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
                    productos.append(getsetProducto(item[0], item[1], item[2], item[3], imagenes, False, 5, item[4],
                                                    item[5], 5000, True, titulo, item[6], item[7], interaccionConUsuario))
            CURSOR.close()
        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

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
                rutasImagenes.append(row.fetchall())

            CURSOR.close()
            self.desconectar_mysql()

        except mysql.connector.errors.ProgrammingError as e:
            print("Error en el procedimiento ", e)
        except Exception as error:
            print("ERROR: ", error)

        return rutasImagenes
