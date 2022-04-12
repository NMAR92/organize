from datos.base_de_datos import BaseDeDatos

def crear_horario_emp(actividad, fecha, hora, nivel_prioridad, insumo):
    id_sesion_sql = f"""
            SELECT ID FROM sesiones ORDER BY ID DESC LIMIT 1
        """
    bd = BaseDeDatos()
    sesion_id = bd.ejecutar_sql(id_sesion_sql)[0][0]

    obtener_sesion_sql = f"""
             SELECT USUARIO_ID FROM sesiones WHERE SESIONES.ID = '{sesion_id}'
        """
    bd = BaseDeDatos()
    usuario_id_sesion = bd.ejecutar_sql(obtener_sesion_sql)[0][0]

    crear_horario_emp_sql = f"""
        INSERT INTO agendar_emp(ACTIVIDAD, FECHA, HORA, NIVEL_PRIORIDAD, INSUMO, USUARIO_ID)
        VALUES ('{actividad}','{fecha}', '{hora}', '{nivel_prioridad}', '{insumo}', '{usuario_id_sesion}')
    """
    bd = BaseDeDatos()
    bd.insert_sql(crear_horario_emp_sql)

def borrar_horario_emp(agendar_emp_id):
    borrar_horario_emp_sql = f"""
        DELETE FROM agendar_emp
        WHERE agendar_emp.AGENDAR_EMP_ID='{agendar_emp_id}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(borrar_horario_emp_sql)

def actualizar_horario_emp(actividad, fecha, hora, nivel_prioridad, insumo, agendar_emp_id):
    actualizar_horario_emp_sql = f"""
        UPDATE agendar_emp
        SET ACTIVIDAD='{actividad}', FECHA='{fecha}', HORA='{hora}', NIVEL_PRIORIDAD='{nivel_prioridad}', INSUMO='{insumo}'
        WHERE agendar_emp.AGENDAR_EMP_ID='{agendar_emp_id}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(actualizar_horario_emp_sql)


def agenda_cli_emp():
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

    obtener_empresa_sql = f"""
                     SELECT NOMBRE FROM registro WHERE registro.USUARIO_ID = '{usuario_id_sesion}'
                """
    bd = BaseDeDatos()
    nombre_empresa_sesion = bd.ejecutar_sql(obtener_empresa_sql)[0][0]

    agenda_cli_emp_sql = f"""
                    SELECT FECHA_HORA, NOMBRE FROM agendar_cli INNER JOIN registro ON agendar_cli.USUARIO_ID=registro.USUARIO_ID WHERE agendar_cli.EMPRESA='{nombre_empresa_sesion}'
                    """
    bd = BaseDeDatos()
    return [{"fecha_hora": registro[0],
             "usuario_id": registro[1]
             } for registro in bd.ejecutar_sql(agenda_cli_emp_sql)]


def obtener_agenda_emp():
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

    obtener_agenda_cli_sql = f"""
                    SELECT ACTIVIDAD, FECHA, HORA, NIVEL_PRIORIDAD, INSUMO, AGENDAR_EMP_ID FROM agendar_emp WHERE agendar_emp.USUARIO_ID = '{usuario_id_sesion}' ORDER BY NIVEL_PRIORIDAD ASC
                   """
    bd = BaseDeDatos()
    return [{"actividad": registro[0],
             "fecha": registro[1],
             "hora": registro[2],
             "nivel_prioridad": registro[3],
             "insumo": registro[4],
             "agendar_emp_id": registro[5]
             } for registro in bd.ejecutar_sql(obtener_agenda_cli_sql)]









