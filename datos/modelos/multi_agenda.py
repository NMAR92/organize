from datos.base_de_datos import BaseDeDatos
def crear_oferta_agenda(hora_inicio, min_inicio, hora_final, min_final, duracion_agenda, dias_semana):
    id_sesion_sql = f"""
        SELECT ID FROM sesiones ORDER BY ID DESC LIMIT 1
    """
    bd = BaseDeDatos()
    sesion_id = bd.ejecutar_sql(id_sesion_sql)[0][0]

    obtener_sesion_sql = f"""
         SELECT USUARIO_ID FROM sesiones WHERE SESIONES.ID = '{sesion_id}'
    """
    bd = BaseDeDatos()
    usuario_id_sesion=bd.ejecutar_sql(obtener_sesion_sql)[0][0]

    crear_oferta_agenda_sql = f"""
        INSERT INTO agendar_ofer(HORA_INICIO, MIN_INICIO, HORA_FINAL, MIN_FINAL, DURACION_AGENDA, DIAS_SEMANA, USUARIO_ID)
        VALUES ('{hora_inicio}','{min_inicio}', '{hora_final}', '{min_final}', '{duracion_agenda}', '{dias_semana}', '{usuario_id_sesion}')
    """
    bd = BaseDeDatos()
    bd.insert_sql(crear_oferta_agenda_sql)


def seleccionar_oferta_agenda(empresa):
    obtener_usuario_id_empresa_sql = f"""
        SELECT USUARIO_ID FROM registro WHERE registro.NOMBRE = '{empresa}'
        """
    bd = BaseDeDatos()
    usuario_id_empresa = bd.ejecutar_sql(obtener_usuario_id_empresa_sql)[0][0]

    seleccionar_oferta_agenda_sql = f"""
        SELECT HORA_INICIO, MIN_INICIO, HORA_FINAL, MIN_FINAL, DURACION_AGENDA, DIAS_SEMANA FROM agendar_ofer WHERE agendar_ofer.USUARIO_ID = '{usuario_id_empresa}'
        """
    bd = BaseDeDatos()
    al=[{"hora_inicio": registro[0],
         "min_inicio": registro[1],
         "hora_final": registro[2],
         "min_final": registro[3],
         "duracion_agenda": registro[4],
         "dias_semana": registro[5]
             } for registro in bd.ejecutar_sql(seleccionar_oferta_agenda_sql)]

# SELECCION DE HORARIOS DE CLIENTES YA TOMADOS PARA ESA EMPRESA

    horarios_tomados_sql = f"""
        SELECT FECHA_HORA FROM agendar_cli WHERE agendar_cli.EMPRESA = '{empresa}'
        """
    bd = BaseDeDatos()
    tom = []
    for registro in bd.ejecutar_sql(horarios_tomados_sql):
        tom.append(registro[0])

# inmutable es que solo se ofrece agenda para proximos 5 dias (de corrido) y las horas de inicio y final de jornada si o si son cada 15 min
    from datetime import timedelta, datetime

    inicio = datetime.today()
    final = inicio + timedelta(days=7)


    Inicio_ano = inicio.strftime('%Y')
    Inicio_mes = inicio.strftime('%m')
    Inicio_dia = inicio.strftime('%d')
    Final_ano = final.strftime('%Y')
    Final_mes = final.strftime('%m')
    Final_dia = final.strftime('%d')

    from datetime import datetime, timedelta

    def datetime_range_day(start, end, d_days, d_minutes):
        current = start
        delta = timedelta(days=d_days, minutes=d_minutes)
        while current < end:
            yield current
            current += delta

    start = datetime(int(Inicio_ano), int(Inicio_mes), int(Inicio_dia))
    end = datetime(int(Final_ano), int(Final_mes), int(Final_dia))

    dias = []
    def d_dia(a):
        for dt in datetime_range_day(start, end, 0, 15):
            if dt.weekday() in range(a):
                dias.append(dt.strftime("%d/%m/%Y, %H:%M"))


    def datetime_range_agenda(start, end, d_minutes):
        current = start
        delta = timedelta(minutes=d_minutes)
        while current < end:
            yield current
            current += delta

    #los horarios de inicio y final de jornada si o si son cada 15min

    horarios_inicio = []
    def horario_inicio(h_inicio, m_inicio):
        for i in dias:
            a = datetime.strptime(i, "%d/%m/%Y, %H:%M")
            if int(a.strftime('%H')) == h_inicio:
                if int(a.strftime('%M')) == m_inicio:
                    horarios_inicio.append(a.strftime("%d/%m/%Y, %H:%M"))

    horarios_final = []
    def horario_final(h_final, m_final):
        for i in dias:
            a = datetime.strptime(i, "%d/%m/%Y, %H:%M")
            if int(a.strftime('%H')) == h_final:
                if int(a.strftime('%M')) == m_final:
                    horarios_final.append(a.strftime("%d/%m/%Y, %H:%M"))

    agendas = []
    agendas_posta = []
    agendas_restar = []

    list= []
    list2= []
    list3= []

    def agendas_ofrecer(minutos_ag):
        for a in horarios_inicio:
            A = datetime.strptime(a, "%d/%m/%Y, %H:%M")
            list.append(A)
        for b in horarios_final:
            B = datetime.strptime(b, "%d/%m/%Y, %H:%M")
            list2.append(B)
        for i in range(len(list)):
            list3.append([list[i], list2[i]])
        for e in range(len(list3)):
            for dt in datetime_range_agenda(list3[e][0], list3[e][1], minutos_ag):
                agendas.append(dt.strftime("%d/%m/%Y, %H:%M"))
        for i in agendas:
            a = datetime.strptime(i, "%d/%m/%Y, %H:%M")
            if int(a.strftime('%d')) == int(inicio.strftime('%d')):
                if int(a.strftime('%H')) < int(inicio.strftime('%H')):
                    agendas_restar.append(a.strftime("%d/%m/%Y, %H:%M"))
                if int(a.strftime('%H')) == int(inicio.strftime('%H')):
                    if int(a.strftime('%M')) < int(inicio.strftime('%M')):
                        agendas_restar.append(a.strftime("%d/%m/%Y, %H:%M"))
        for a in agendas:
                if a not in agendas_restar:
                    agendas_posta.append(a)
        for a in tom:
            if a in agendas_posta:
                agendas_posta.remove(a)

    d_dia(al[0]["dias_semana"])
    horario_inicio(al[0]["hora_inicio"],al[0]["min_inicio"])
    horario_final(al[0]["hora_final"],al[0]["min_final"])
    agendas_ofrecer(al[0]["duracion_agenda"])


    return {"agenda": agendas_posta}


def borrar_oferta_agenda(agendar_ofer_id):
    borrar_oferta_agenda_sql = f"""
        DELETE FROM agendar_ofer
        WHERE agendar_ofer.AGENDAR_OFER_ID='{agendar_ofer_id}'
    """
    bd = BaseDeDatos()
    bd.insert_sql(borrar_oferta_agenda_sql)

def actualizar_oferta_agenda(hora_inicio, min_inicio, hora_final, min_final, duracion_agenda, dias_semana, agendar_ofer_id):
    actualizar_oferta_agenda_sql = f"""
        UPDATE agendar_ofer
        SET HORA_INICIO='{hora_inicio}', MIN_INICIO='{min_inicio}', HORA_FINAL='{hora_final}', MIN_FINAL='{min_final}', DURACION_AGENDA ='{duracion_agenda}', DIAS_SEMANA='{dias_semana}'
        WHERE (AGENDAR_OFER_ID='{agendar_ofer_id}')
    """
    bd = BaseDeDatos()
    bd.insert_sql(actualizar_oferta_agenda_sql)

def obtener_oferta_agenda():
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

    obtener_oferta_agenda_sql = f"""
                    SELECT HORA_INICIO, MIN_INICIO, HORA_FINAL, MIN_FINAL, DURACION_AGENDA, DIAS_SEMANA, USUARIO_ID, AGENDAR_OFER_ID FROM agendar_ofer WHERE agendar_ofer.USUARIO_ID = '{usuario_id_sesion}'
                   """
    bd = BaseDeDatos()
    return [{"hora_inicio": registro[0],
         "min_inicio": registro[1],
         "hora_final": registro[2],
         "min_final": registro[3],
         "duracion_agenda": registro[4],
         "dias_semana": registro[5],
         "agendar_ofer_id": registro[6]
             } for registro in bd.ejecutar_sql(obtener_oferta_agenda_sql)]