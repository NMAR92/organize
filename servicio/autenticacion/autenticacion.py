from datos.modelos import usuario as modelo_usuario
from datetime import datetime
import logging


def crear_usuario(nombre, clave, mail,tipo_suscripcion_id):
    modelo_usuario.crear_usuario(nombre, clave, mail, tipo_suscripcion_id)

def borrar_usuario(mail):
    modelo_usuario.borrar_usuario(mail)

def consulta_mail(mail):
    x = modelo_usuario.consulta_mail(mail)
    if len(x) == 0:
        return {"mail": "str"}
    else:
        return x[0]

def validar_mail():
    return modelo_usuario.validar_mail()[0]

def actualizar_usuario( nombre, mail, clave):
    modelo_usuario.actualizar_usuario(nombre, mail, clave)

def obtener_usuarios():
    return modelo_usuario.obtener_usuarios()

def obtener_usuario_t(usuario_id):
    x = modelo_usuario.obtener_usuario_t(usuario_id)
    if len(x) == 0:
        return "El usuario no existe"
    else:
        return x[0]

def obtener_usuario(mail):
    x = modelo_usuario.obtener_usuario(mail)
    if len(x) == 0:
        return "El usuario no existe"
    else:
        return x[0]

def obtener_empresas():
    return modelo_usuario.obtener_empresas()

def _existe_usuario(mail, clave):
    usuarios = modelo_usuario.obtener_usuarios_por_mail_clave(mail, clave)
    return not len(usuarios) == 0

def login(mail, clave):
    if _existe_usuario(mail, clave):
        usuario = modelo_usuario.obtener_usuarios_por_mail_clave(mail, clave)[0]
        logging.exception(usuario)
        return _crear_sesion(usuario['usuario_id'])


def _crear_sesion(id_usuario):
    hora_actual = datetime.now()
    dt_string = hora_actual.strftime("%d/%m/%Y %H:%M:%S")
    return modelo_usuario.crear_sesion(id_usuario, dt_string)

def obtener_sesion():
    sesiones = modelo_usuario.obtener_sesion()
    if len(sesiones) == 0:
        return "La sesion no existe"
    else:
        return sesiones[0]

def crear_mensaje(nombre, mail, mensaje):
    modelo_usuario.crear_mensaje(nombre, mail, mensaje)