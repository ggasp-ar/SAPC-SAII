from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from .models.ModeloCompra import ModeloCompra
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario

from .models.entities.Compra import Compra
from .models.entities.Libro import Libro
from .models.entities.Usuario import Usuario

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
        usuario = Usuario(None, request.form['usuario'], request.form['password'], None, None)
        usuario_logeado = ModeloUsuario.login(db, usuario)
        if usuario_logeado != None:
            login_user(usuario_logeado)
            flash('Bienvenido {}'.format(usuario_logeado.usuario), 'success')
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
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos = ModeloLibro.obtener_libros_vendidos(db)
                data = {
                    'titulo': 'Libros Vendidos',
                    'libros_vendidos': libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as e:
                return render_template('errores/error.html')
        else:
            try:
                compras = ModeloCompra.obtener_compras_por_usuario(db, current_user)
                data = {
                    'titulo': 'Mis compras',
                    'compras': compras
                }
                return render_template('index.html', data=data)
            except Exception as e:
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
    
@app.route('/libros')
@login_required
def listar_libros():
    try:
        libros=ModeloLibro.listar_libros(db)
        data = {
            'titulo': 'Listado de Libros',
            'libros': libros
            }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        return render_template('errores/error.html')

@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()
    data={}
    try:
        # libro = Libro(data_request['isbn'],None,None,None,None)
        libro = ModeloLibro.leer_libro(db,data_request['isbn'])
        compra = Compra(None,libro,current_user)
        data['exito'] = ModeloCompra.registrar_compra(db,compra)
    except Exception as ex:
        data['mensaje']=format(ex)
        data['exito']=False

    return jsonify(data)

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