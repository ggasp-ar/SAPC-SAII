from distutils.log import debug
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from app.models.ModeloCuenta import ModeloCuenta

from .models.ModeloUsuario import ModeloUsuario
from .models.entities.Usuario import Usuario
from .utils import debugPrint

from .consts import *


app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db, id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        usuario_id = ModeloUsuario.login(db, 
                            usr=request.form['usuario'],
                            pwd=request.form['password'])
        if usuario_id != None:
            usuario = ModeloUsuario.obtener_por_id(db,usuario_id)
            login_user(usuario)
            flash('Bienvenido {}'.format(usuario.nombre), 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESINVALIDAS,'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/verasiento')
@login_required
def ver_asiento():
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))
    try:
        #aca iria la logica de traer el asiento (id) desde la DB
        asientos = [["Caja",15000,0],
                    ["Proveedoreaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas",42000,1]]
        data = {
            'titulo': 'Asiento',
            'id': '1234',
            'asientos': asientos
        }
        return render_template('asientos/ver_asiento.html', data=data)
    except Exception as e:
        return render_template('errores/error.html')

@app.route('/registrarasiento')
@login_required
def registrar_asiento():
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))
    try:
        asientos = [["Caja",15000,0],
                    ["Proveedores",42000,1]]
        data = {
            'titulo': 'Asiento',
            'id': '0',
            'asientos': [["Caja",15000,0]]
        }
        return render_template('asientos/registrar_asiento.html', data=data)
    except Exception as e:
        debugPrint(e, "Registrar Asiento")
        return render_template('errores/error.html')

@app.route('/cargarasiento', methods=['POST'])
def cargar_asiento():
    data = request.get_json()
    debugPrint(data,"cargarasiento")
    return jsonify({'exito':False,'mensaje':'Todavia no esta implementada la carga de asientos'})

@app.route('/cuentas')
@login_required
def ver_cuentas():
    familia_cuentas=ModeloCuenta().generarArbol(db)
    debugPrint(familia_cuentas,"ver_cuentas")
    return render_template('cuentas/cuentas.html',data=familia_cuentas)


@app.route('/crearusuario', methods=['GET', 'POST'])
def crearusuario():
    if request.method == 'POST':
        nuevoUsuario = (request.form['usuario'],request.form['password'],request.form['passwordTwo'])
        usuario_creado = ModeloUsuario.crear_usuario(db, nuevoUsuario)
        if usuario_creado != None:
            flash('Usuario creado correctamente', 'success')
            return redirect(url_for('login'))
        else:
            flash('Las Contraseñas no coinciden', 'warning')
            return render_template('auth/crearusuario.html')
    else:
        return render_template('auth/crearusuario.html')
    

def pagina_no_encontrada(error):
    return render_template('errores/418.html'), 404

def pagina_no_autorizada(error):
    return redirect(url_for('login'))

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada) #418
    app.register_error_handler(401, pagina_no_autorizada)
    return app