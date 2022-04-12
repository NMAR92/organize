from datos.base_de_datos import BaseDeDatos
import logging


def crear_usuario(nombre, clave, mail, tipo_suscripcion_id):
    crear_usuario_sql = f"""
        INSERT INTO registro (NOMBRE, CLAVE, MAIL, TIPO_SUSCRIPCION_ID )
        VALUES ('{nombre}','{clave}','{mail}', '{tipo_suscripcion_id}')
    """
    bd = BaseDeDatos()
    bd.insert_sql(crear_usuario_sql)

def borrar_usuario(mail):
    borrar_usuario_sql = f"""
        DELETE FROM registro WHERE registro.MAIL = '{mail}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(borrar_usuario_sql)

def consulta_mail(mail):
    consulta_mail_sql = f"""
            SELECT MAIL FROM registro WHERE registro.MAIL = '{mail}'
        """
    bd = BaseDeDatos()
    return [{'mail': registro[0]
             } for registro in bd.ejecutar_sql(consulta_mail_sql)]

def validar_mail():
    id_sesion_sql = f"""
            SELECT ID FROM sesiones ORDER BY ID DESC LIMIT 1
        """
    bd = BaseDeDatos()
    sesion_id = bd.ejecutar_sql(id_sesion_sql)[0][0]

    obtener_sesion_sql = f"""
             SELECT USUARIO_ID FROM sesiones WHERE sesiones.ID = '{sesion_id}'
        """
    bd = BaseDeDatos()
    usuario_id_sesion = bd.ejecutar_sql(obtener_sesion_sql)[0][0]

    mail_sesion_sql = f"""
        SELECT MAIL FROM registro WHERE registro.USUARIO_ID = '{usuario_id_sesion}'
    """
    bd = BaseDeDatos()
    return [{"mail": registro[0]
             } for registro in bd.ejecutar_sql(mail_sesion_sql)]

def actualizar_usuario(nombre, clave, mail):
    actualizar_usuario_sql = f"""
        UPDATE registro SET NOMBRE = '{nombre}', CLAVE = '{clave}' WHERE registro.MAIL='{mail}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(actualizar_usuario_sql)


def obtener_usuario_t(usuario_id):
    obtener_usuario_t_sql = f"""
        SELECT NOMBRE, USUARIO_ID, TIPO_SUSCRIPCION_ID, MAIL
        FROM registro
        WHERE registro.USUARIO_ID='{usuario_id}'
    """
    bd = BaseDeDatos()
    return [{"nombre": registro[0],
             "usuario_id": registro[1],
             "tipo_suscripcion_id": registro[2],
             "mail": registro[3]
             } for registro in bd.ejecutar_sql(obtener_usuario_t_sql)]

def obtener_usuario(mail):
    obtener_usuario_sql = f"""
        SELECT NOMBRE, USUARIO_ID, TIPO_SUSCRIPCION_ID, MAIL
        FROM registro
        WHERE registro.MAIL='{mail}'
    """
    bd = BaseDeDatos()
    return [{"nombre": registro[0],
             "usuario_id": registro[1],
             "tipo_suscripcion_id": registro[2],
             "mail": registro[3]
             } for registro in bd.ejecutar_sql(obtener_usuario_sql)]

def obtener_usuarios():
    obtener_usuarios_sql = f"""
        SELECT NOMBRE, USUARIO_ID, TIPO_SUSCRIPCION_ID
        FROM registro
    """
    bd = BaseDeDatos()
    return [{"nombre": registro[0],
             "usuario_id": registro[1],
             "tipo_suscripcion_id": registro[2]
             } for registro in bd.ejecutar_sql(obtener_usuarios_sql)]

def obtener_empresas():
    obtener_empresas_sql = f"""
        SELECT NOMBRE
        FROM registro
        WHERE registro.TIPO_SUSCRIPCION_ID='2'
    """
    bd = BaseDeDatos()
    return [{"nombre": registro[0],
             } for registro in bd.ejecutar_sql(obtener_empresas_sql)]


def obtener_usuarios_por_mail_clave(mail, clave):
    obtener_usuario_sql = f"""
            SELECT USUARIO_ID, NOMBRE, TIPO_SUSCRIPCION_ID
            FROM registro
            WHERE registro.MAIL='{mail}' and registro.CLAVE='{clave}'
    """
    bd = BaseDeDatos()
    return [{"usuario_id": registro[0],
             "nombre": registro[1],
             "tipo_suscripcion_id": registro[2]
             } for registro in bd.ejecutar_sql(obtener_usuario_sql)]



def crear_sesion(id_usuario, dt_string):
    crear_sesion_sql = f"""
               INSERT INTO sesiones(USUARIO_ID, FECHA_HORA)
               VALUES ('{id_usuario}', '{dt_string}')
    """
    bd = BaseDeDatos()
    #a= bd.insert_sql("INSERT INTO sesiones(USUARIO_ID, FECHA_HORA, ID) VALUES ('5', '5', '0')")
    #logging.exception(a)
    #row = bd.ejecutar_sql("SELECT * FROM sesiones")
    #logging.exception(row)
    #b= bd.ejecutar_sql("SELECT * FROM sesiones")
    #logging.exception(b)
    bd.insert_sql(crear_sesion_sql)

    id_sesion_sql = f"""
        SELECT ID FROM sesiones ORDER BY ID DESC LIMIT 1
    """
    bd = BaseDeDatos()
    return bd.ejecutar_sql(id_sesion_sql)[0][0]

def obtener_sesion():
    id_sesion_sql = f"""
        SELECT ID FROM sesiones ORDER BY ID DESC LIMIT 1
    """
    bd = BaseDeDatos()
    sesion_id = bd.ejecutar_sql(id_sesion_sql)[0][0]

    obtener_sesion_sql = f"""
         SELECT ID, USUARIO_ID, FECHA_HORA FROM sesiones WHERE (ID = '{sesion_id}')
    """
    bd = BaseDeDatos()
    return [{"id": registro[0],
            "usuario_id": registro[1],
            "fecha_hora": registro[2]
            } for registro in bd.ejecutar_sql(obtener_sesion_sql)]

def crear_mensaje(nombre, mail, mensaje):
    id_sesion_sql = f"""
        SELECT ID FROM sesiones ORDER BY ID DESC LIMIT 1
    """
    bd = BaseDeDatos()
    sesion_id = bd.ejecutar_sql(id_sesion_sql)[0][0]

    obtener_sesion_sql = f"""
         SELECT USUARIO_ID FROM sesiones WHERE sesiones.ID = '{sesion_id}'
    """
    bd = BaseDeDatos()
    usuario_id_sesion=bd.ejecutar_sql(obtener_sesion_sql)[0][0]

    crear_mensaje_sql = f"""
        INSERT INTO mensajes (NOMBRE, MAIL, MENSAJE, USUARIO_ID)
        VALUES ('{nombre}','{mail}', '{mensaje}', '{usuario_id_sesion}')
    """
    bd = BaseDeDatos()
    bd.insert_sql(crear_mensaje_sql)
