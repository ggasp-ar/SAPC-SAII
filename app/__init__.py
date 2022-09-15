from distutils.log import debug
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

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
        usuario = ModeloUsuario.login(db, 
                            usr=request.form['usuario'],
                            pwd=request.form['password'])
        if usuario != None:
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
    if current_user.is_authenticated:
        try:
            debugPrint(current_user.info)
            return redirect(url_for('registrar_asiento'))
        except Exception as e:
            debugPrint(e)
            return render_template('errores/error.html')
    else:
        return redirect(url_for('login'))

@app.route('/registrar_asiento')
@login_required
def registrar_asiento():
    debugPrint(current_user.info)
    if current_user.is_authenticated:
        try:
            asientos = [["Caja",15000,0],
                        ["Proveedores",42000,1]]
            data = {
                'titulo': 'Asientos...',
                'asientos': asientos
            }
            return render_template('registrar_asiento.html', data=data)
        except Exception as e:
            debugPrint(e)
            return render_template('errores/error.html')
    else:
        return redirect(url_for('login'))

@app.route('/crearusuario', methods=['GET', 'POST'])
def crearusuario():
    if request.method == 'POST':
        nuevoUsuario = (request.form['usuario'],request.form['password'],request.form['passwordTwo'],request.form['Celulular'])
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