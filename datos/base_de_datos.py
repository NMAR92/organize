import mysql.connector

class BaseDeDatos:

    def _crear_conexion(self):
        try:
            self.conexion = mysql.connector.connect( user='organize', password= 'colorado1234*', host='organize.mysql.pythonanywhere-services.com', database='organize$organize')
        except Exception as e:
            print(e)

    def _cerrar_conexion(self):
        self.conexion.close()
        self.conexion = None

    def ejecutar_sql(self, sql):
        self._crear_conexion()
        cur = self.conexion.cursor()
        cur.execute(sql)

        filas = cur.fetchall()

        self.conexion.commit()
        self._cerrar_conexion()

        return filas

    def insert_sql(self, sql):
        self._crear_conexion()
        cur = self.conexion.cursor()
        cur.execute(sql)

        filas = cur.fetchone()

        self.conexion.commit()
        self._cerrar_conexion()

        return filas

