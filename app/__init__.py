from distutils.log import debug
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models.ModeloAsiento import ModeloAsiento

from app.models.ModeloCuenta import ModeloCuenta
from app.models.ModeloTipoCuenta import ModeloTipoCuenta
from app.models.entities.Cuenta import Cuenta

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
            try:
                usuario = ModeloUsuario.obtener_por_id(db,usuario_id)
                login_user(usuario)
                flash('Bienvenido {}'.format(usuario.nombre), 'success')
                return redirect(url_for('index'))
            except:
                flash('Por favor, verifique sus datos','warning')
                return render_template('auth/login.html')
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
    args = request.args
    MA = ModeloAsiento()
    MU = ModeloUsuario()
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))
    try:
        asiento = MA.obtenerAsiento(db, args.get("asiento_id"))
        fecha = asiento.getFecha().replace(' ', 'T').rsplit(':',1)[0]
        responsable = MU.obtener_por_id(db, asiento.getResponsable())
        data = {
            'titulo': asiento.getDesc(),
            'id': asiento.getId(),
            'fecha': fecha,
            'responsable': responsable.nombre,
            'responsableid': asiento.getResponsable(),
            'asientos': asiento.getAsientos()
        }
        return render_template('asientos/ver_asiento.html', data=data)
    except Exception as e:
        return render_template('errores/error.html')

@app.route('/registrarasiento', methods=['GET', 'POST'])
@login_required
def registrar_asiento():
    MA = ModeloAsiento()
    MC = ModeloCuenta()
    if request.method == 'GET':
        if not(current_user.is_authenticated):
            return redirect(url_for('login'))
        try:
            data = {
                'titulo': 'Asiento',
                'id': MA.nextAsientoId(db),
                'responsable': current_user.nombre,
                'responsableid': current_user.id
            }
            return render_template('asientos/registrar_asiento.html', data=data)
        except Exception as e:
            return render_template('errores/error.html')
    else:
        try:
            data = request.get_json()
            
            asiento, cuentas_modificadas = MA.verificarAsiento(MA.crearAsiento(data),
                                                            MC.obtenerCuentasSaldo(db, False))
            debugPrint(cuentas_modificadas, "registrar asiento POST")
            debugPrint(asiento, "registrar asiento POST")
            
            MA.cargarAsiento(db, asiento)
            MC.actualizarCuentas(db, cuentas_modificadas)
            db.connection.commit()
            
            return jsonify({'exito':True,'mensaje':'Asiento Cargado'})
        except Exception as e:
            return jsonify({'exito':False,'mensaje':('Fallo la carga de asientos: ' + str(e))})
        

@app.route('/cuentas', methods=['GET', 'POST'])
@login_required
def ver_cuentas():
    mc=ModeloCuenta()
    if request.method == 'POST':
        cuentas = mc.obtenerCuentasSaldo(db)
        dict_cuentas = mc.obtenerDict(cuentas,True)
        return jsonify(dict_cuentas)
    else:
        return render_template('cuentas/cuentas.html',data=mc.generarArbol(db))

@app.route('/registrarcuenta', methods=['POST'])
@login_required
def registrar_cuenta():
    MC = ModeloCuenta()
    MTC = ModeloTipoCuenta()
    try:
        data = request.get_json()
        nuevaCuenta = Cuenta(id= None,
                            codigo= data['codigo'],
                            nombre= data['cuenta'],
                            saldo= 0,
                            tipo= MTC.obtenerTipo(db,data['tipo']),
                            recibe= data['recibe'],
                            padreid= data['padre_cid']
                            )
        print(nuevaCuenta.getPadre().getCodigo())
        debugPrint(nuevaCuenta, "nueva cuenta creada")
        #MC.cargarNuevaCuenta(db, nuevaCuenta)
        return jsonify({'exito':True,'mensaje':'Cuenta Creada'})
    except Exception as e:
        return jsonify({'exito':False,'mensaje':('Fallo la creacion de la nueva cuenta: ' + str(e))})

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