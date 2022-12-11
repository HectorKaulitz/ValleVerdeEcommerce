import mysql.connector


class MySQL:

    def __init__(self, host="localhost", user="root", pws="", bd="valleverdeecommerce"):
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
