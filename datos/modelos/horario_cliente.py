from datos.base_de_datos import BaseDeDatos

def crear_horario_cliente(empresa, fecha_hora):
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

    crear_horario_cliente_sql = f"""
        INSERT INTO agendar_cli(EMPRESA, FECHA_HORA, USUARIO_ID)
        VALUES ('{empresa}','{fecha_hora}', '{usuario_id_sesion}')
    """
    bd = BaseDeDatos()
    bd.insert_sql(crear_horario_cliente_sql)

def borrar_horario_cliente(agendar_cli_id):
    borrar_horario_cliente_sql = f"""
        DELETE FROM agendar_cli
        WHERE agendar_cli.AGENDAR_CLI_ID='{agendar_cli_id}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(borrar_horario_cliente_sql)

def actualizar_horario_cliente(empresa, fecha_hora, agendar_cli_id):
    actualizar_horario_cliente_sql = f"""
        UPDATE agendar_cli
        SET EMPRESA='{empresa}', FECHA_HORA='{fecha_hora}'
        WHERE agendar_cli.AGENDAR_CLI_ID='{agendar_cli_id}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(actualizar_horario_cliente_sql)

def obtener_agenda_cli():
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
                    SELECT EMPRESA, FECHA_HORA, AGENDAR_CLI_ID FROM agendar_cli WHERE  agendar_cli.USUARIO_ID = '{usuario_id_sesion}'
                   """
    bd = BaseDeDatos()
    return [{"empresa": registro[0],
             "fecha_hora": registro[1],
             "agendar_cli_id": registro[2]
             } for registro in bd.ejecutar_sql(obtener_agenda_cli_sql)]










