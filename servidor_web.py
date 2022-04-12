
from flask import Flask, request, redirect, url_for, session
from flask import render_template
from datos.modelos import usuario
from servicio.autenticacion import autenticacion
from servicio.cliente import cliente
from servicio.emprendedor import emprendedor
from servicio.multi_agenda import multi_agenda

app = Flask(__name__, template_folder='templates')

SECRET_KEY = 'kajsnxanxkanxkna'
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

##########################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['mail'] = request.form['mail']
        if not autenticacion.login(request.form['mail'], request.form['clave']):
            error = 'Usuario y/o contraseña incorrecta'
        else:
            if autenticacion.obtener_usuario(request.form['mail'])['tipo_suscripcion_id'] == 1:
                return redirect(url_for('inicio_cliente'))
            else:
                return redirect(url_for('inicio_emp'))
    return render_template('login.html', error=error)

#######################################################
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    error = None
    if request.method == 'POST':
         if len(usuario.consulta_mail(request.form['mail'])) != 0:
             error = 'Ya existe una cuenta con este mail'
         else:
            usuario.crear_usuario(request.form['nombre'], request.form['clave'], request.form['mail'], request.form['tipo_suscripcion_id'])
            return redirect(url_for('login'))
    return render_template('registro.html', error=error)
#########################################################
@app.route('/actualizar_usuario',  methods=['GET', 'POST'])
def actualizar_usuario():
    if not session:
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        if not autenticacion.validar_mail()['mail'] == request.form['mail']:
            error = 'El mail ingresado no es con el que se inicio sesión'
        else:
            autenticacion.actualizar_usuario(request.form['nombre'], request.form['mail'], request.form['clave'])
            if autenticacion.obtener_usuario(request.form['mail'])['tipo_suscripcion_id'] == 1:
                return redirect(url_for('inicio_cliente'))
            else:
                return redirect(url_for('inicio_emp'))
    return render_template('actualizar_usuario.html', error=error)

########################################
@app.route('/borrar_usuario',  methods=['GET', 'POST'])
def borrar_usuario():
    error = None
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if not autenticacion.validar_mail()['mail'] == request.form['mail']:
            error = 'El mail ingresado no es con el que se inicio sesión'
        else:
            autenticacion.borrar_usuario(request.form['mail'])
            return redirect(url_for('login'))
    return render_template('borrar_usuario.html', error=error)

##############################################
@app.route('/formulario_contacto', methods=['GET', 'POST'])
def crear_mensaje():
    error = None
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if not autenticacion.validar_mail()['mail'] == request.form['mail']:
            error = 'El mail ingresado no es con el que se inicio sesión'
        else:
            autenticacion.crear_mensaje(request.form['nombre'], request.form['mail'], request.form['mensaje'])
            if autenticacion.obtener_usuario(session['mail'])['tipo_suscripcion_id'] == 1:
                return redirect(url_for('inicio_cliente'))
            else:
                return redirect(url_for('inicio_emp'))
    return render_template('formulario_contacto.html', error=error)

#######################
@app.route('/nosotros_cli', methods=['GET'])
def nosotros_cli():
    if not session:
        return redirect(url_for('login'))
    return render_template('nosotros_cli.html')

#############################
@app.route('/nosotros_emp', methods=['GET'])
def nosotros_emp():
    if not session:
        return redirect(url_for('login'))
    return render_template('nosotros_emp.html')


##CLIENTE##
#################################
@app.route('/fecha_hora', methods=['GET', 'POST'])
def fecha_hora():
    if not session:
        return redirect(url_for('login'))
    usuario = autenticacion.obtener_usuario_t(autenticacion.obtener_sesion()['usuario_id'])
    output = request.get_json()
    if request.method == 'POST':
        fecha_horas = multi_agenda.seleccionar_oferta_agenda(output['empresa'])
        print(fecha_horas['agenda'])
        return fecha_horas
    return render_template('inicio_cliente.html', usuario=usuario)

#############################################################
@app.route('/inicio_cliente', methods=['GET', 'POST'])
def inicio_cliente():
    if not session:
        return redirect(url_for('login'))
    empresas = autenticacion.obtener_empresas()
    usuario = autenticacion.obtener_usuario_t(autenticacion.obtener_sesion()['usuario_id'])
    horarios = cliente.obtener_agenda_cli()
    return render_template('inicio_cliente.html', empresas=empresas, usuario=usuario, horarios=horarios)

#######################################################
@app.route('/inicio_cliente/agregar', methods=['POST'])
def agregar_horario_cliente():
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cliente.crear_horario_cliente(request.form['empresa'], request.form['fecha_hora'])
    return redirect(url_for('inicio_cliente'))

###########################################################
@app.route('/inicio_cliente/<agendar_cli_id>/eliminar', methods=['POST'])
def eliminar_horario_cliente(agendar_cli_id):
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cliente.borrar_horario_cliente(agendar_cli_id)
    return redirect(url_for('inicio_cliente'))

############################################################
@app.route('/inicio_cliente/<agendar_cli_id>/editar', methods=['GET', 'POST'])
def editar_horario_cliente(agendar_cli_id):
    if not session:
        return redirect(url_for('login'))
    empresas = autenticacion.obtener_empresas()
    if request.method == 'POST':
        cliente.actualizar_horario_cliente(request.form['empresa'], request.form['fecha_hora'], agendar_cli_id)
        return redirect(url_for('inicio_cliente'))
    return render_template('editar_cliente.html', empresas=empresas, agendar_cli_id=agendar_cli_id)


## EMPRENDEDOR ##
##########################################################
@app.route('/inicio_emp')
def inicio_emp():
    if not session:
        return redirect(url_for('login'))
    usuario = autenticacion.obtener_usuario_t(autenticacion.obtener_sesion()['usuario_id'])
    cli_horarios = emprendedor.agenda_cli_emp()
    return render_template('inicio_emp.html', usuario=usuario, cli_horarios=cli_horarios)

##SEGUNDA TABLA EMP##

@app.route('/inicio_emp_emp')
def inicio_emp_emp():
    if not session:
        return redirect(url_for('login'))
    usuario = autenticacion.obtener_usuario_t(autenticacion.obtener_sesion()['usuario_id'])
    horarios = emprendedor.obtener_agenda_emp()
    return render_template('inicio_emp_emp.html', usuario=usuario, horarios=horarios)


@app.route('/inicio_emp_emp/agregar', methods=['POST'])
def agregar_horario_emp_emp():
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        emprendedor.crear_horario_emp(request.form['actividad'], request.form['fecha'], request.form['hora'], request.form['nivel_prioridad'], request.form['insumo'])
    return redirect(url_for('inicio_emp_emp'))


@app.route('/inicio_emp_emp/<agendar_emp_id>/eliminar', methods=['POST'])
def eliminar_horario_emp_emp(agendar_emp_id):
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        emprendedor.borrar_horario_emp(agendar_emp_id)
    return redirect(url_for('inicio_emp_emp'))


@app.route('/inicio_emp_emp/<agendar_emp_id>/editar', methods=['GET', 'POST'])
def editar_horario_emp_emp(agendar_emp_id):
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        emprendedor.actualizar_horario_emp(request.form['actividad'], request.form['fecha'], request.form['hora'], request.form['nivel_prioridad'], request.form['insumo'], agendar_emp_id)
        return redirect(url_for('inicio_emp_emp'))
    return render_template('editar_emp.html', agendar_emp_id=agendar_emp_id)

#FORMATO DE AGENDA DEL EMPRENDEDOR A OFRECER A CLIENTES

@app.route('/inicio_ag_emp')
def inicio_ag_emp():
    if not session:
        return redirect(url_for('login'))
    usuario = autenticacion.obtener_usuario_t(autenticacion.obtener_sesion()['usuario_id'])
    formatos = multi_agenda.obtener_oferta_agenda()
    return render_template('inicio_ag_emp.html', usuario=usuario, formatos=formatos)

@app.route('/inicio_ag_emp/agregar', methods=['GET', 'POST'])
def agregar_oferta_agenda():
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        multi_agenda.crear_oferta_agenda(request.form['hora_inicio'], request.form['min_inicio'], request.form['hora_final'], request.form['min_final'], request.form['duracion_agenda'], request.form['dias_semana'])
    return redirect(url_for('inicio_ag_emp'))


@app.route('/inicio_ag_emp/<agendar_ofer_id>/eliminar', methods=['POST'])
def eliminar_oferta_agenda(agendar_ofer_id):
    if not session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        multi_agenda.borrar_oferta_agenda(agendar_ofer_id)
    return redirect(url_for('inicio_ag_emp'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not session:
        return redirect(url_for('login'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

