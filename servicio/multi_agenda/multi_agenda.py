from datos.modelos import multi_agenda as m_multi_agenda

def crear_oferta_agenda(hora_inicio, min_inicio, hora_final, min_final, duracion_agenda, dias_semana):
    return m_multi_agenda.crear_oferta_agenda(hora_inicio, min_inicio, hora_final, min_final, duracion_agenda, dias_semana)

def seleccionar_oferta_agenda(empresa):
    return m_multi_agenda.seleccionar_oferta_agenda(empresa)

def borrar_oferta_agenda(agendar_ofer_id):
    return m_multi_agenda.borrar_oferta_agenda(agendar_ofer_id)

def actualizar_oferta_agenda(hora_inicio, min_inicio, hora_final, min_final, duracion_agenda, dias_semana, agendar_ofer_id):
    return m_multi_agenda.actualizar_oferta_agenda(hora_inicio, min_inicio, hora_final, min_final, duracion_agenda, dias_semana, agendar_ofer_id)

def obtener_oferta_agenda():
    return m_multi_agenda.obtener_oferta_agenda()



