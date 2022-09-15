from .entities.Usuario import Usuario
from .entities.TipoUsuario import TipoUsuario

class ModeloUsuario():

    @classmethod
    def login(self,db,usr,pwd):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * 
                    FROM usuarios WHERE usuario = '{0}' """.format(usr)
            cursor.execute(sql)
            data = cursor.fetchone()
            #usuario_id,usuario,nombre,contrasenia,rol_id,habilitada
            if data != None:
                if data[5] != 0:
                    if Usuario.verificar_password(data[3], pwd):
                        usuario_logeado = Usuario(id=data[0],
                                                usuario=data[1],
                                                nombre=data[2],
                                                password=data[3],
                                                rol=data[4])
                        return usuario_logeado
                return None
            else:
                return None
                
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crear_usuario(self,db,nuevoUsuario):
        # validar contraseña
        if nuevoUsuario[1] != nuevoUsuario[2]:
            return None
        try:
            usuario = Usuario(0, nuevoUsuario[0], Usuario.crear_password(nuevoUsuario[1]), 2, nuevoUsuario[3])
            cursor = db.connection.cursor()
            sql = f"""INSERT INTO usuario (id, usuario, password, tipousuario_id, celular)
                    VALUES ('NULL', '{usuario.usuario}', '{usuario.password}', 2, '{usuario.celular}') """
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_por_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT USU.usuario_id, USU.usuario, USU.nombre, TIP.rol_id, TIP.descripcion, USU.habilitada
                    FROM usuarios USU JOIN roles TIP ON USU.rol_id = TIP.rol_id
                    WHERE USU.usuario_id = {0} """.format(id)
            cursor.execute(sql)
            data = cursor.fetchone()
            tipousuario = TipoUsuario(data[2],data[3])
            usuario_logeado = Usuario(id=data[0],
                                    usuario=data[1],
                                    nombre=data[2],
                                    password=None,
                                    rol=data[3])
            return usuario_logeado
        except Exception as ex:
            raise Exception(ex)