
from datos.modelos import horario_cliente as m_horario_cliente


def crear_horario_cliente(empresa, fecha_hora):
    return m_horario_cliente.crear_horario_cliente(empresa, fecha_hora)

def borrar_horario_cliente(agendar_cli_id):
    return m_horario_cliente.borrar_horario_cliente(agendar_cli_id)

def actualizar_horario_cliente(empresa, fecha_hora, agendar_cli_id):
    return m_horario_cliente.actualizar_horario_cliente(empresa, fecha_hora, agendar_cli_id)

def obtener_agenda_cli():
    return m_horario_cliente.obtener_agenda_cli()

