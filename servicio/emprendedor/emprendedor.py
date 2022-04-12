
from datos.modelos import horario_emp as m_horario_emp


def crear_horario_emp(actividad, fecha, hora, nivel_prioridad, insumo):
    return m_horario_emp.crear_horario_emp(actividad, fecha, hora, nivel_prioridad, insumo)

def borrar_horario_emp(agendar_emp_id):
    return m_horario_emp.borrar_horario_emp(agendar_emp_id)

def actualizar_horario_emp(actividad, fecha, hora, nivel_prioridad, insumo, agendar_emp_id):
    return m_horario_emp.actualizar_horario_emp(actividad, fecha, hora, nivel_prioridad, insumo, agendar_emp_id)

def agenda_cli_emp():
    return m_horario_emp.agenda_cli_emp()

def obtener_agenda_emp():
    return m_horario_emp.obtener_agenda_emp()