from .entities.Usuario import Usuario
from .entities.TipoUsuario import TipoUsuario
from ..utils import fetchOne
class ModeloUsuario():

    @classmethod
    def login(self,db,usr,pwd):
        try:
            sql = """SELECT u.usuario_id, u.contrasenia, u.habilitada
                    FROM usuarios u WHERE usuario = '{0}' """.format(usr)
            data = fetchOne(db,sql)
            if data != None:
                if data["habilitada"] != 0 and Usuario.verificar_password(data["contrasenia"], pwd):
                    return data["usuario_id"]
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crear_usuario(self,db,nuevoUsuario):
        return False #Deshabilitado temporalmente
        # validar contraseña
        if nuevoUsuario[1] != nuevoUsuario[2]:
            return None
        try:
            usuario = Usuario(0, nuevoUsuario[0], Usuario.crear_password(nuevoUsuario[1]), 2, nuevoUsuario[3])
            sql = f"""INSERT INTO usuario (id, usuario, password, tipousuario_id, celular)
                    VALUES ('NULL', '{usuario.usuario}', '{usuario.password}', 2, '{usuario.celular}') """
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_por_id(self,db,id):
        try:
            sql = """SELECT USU.usuario_id, USU.usuario, USU.nombre, TIP.rol_id, TIP.descripcion, USU.habilitada
                    FROM usuarios USU JOIN roles TIP ON USU.rol_id = TIP.rol_id
                    WHERE USU.usuario_id = {0} """.format(id)      
            data = fetchOne(db,sql)
            #tipousuario = TipoUsuario(data[2],data[3])
            usuario_logeado = Usuario(id=data["usuario_id"],
                                    usuario=data["usuario"],
                                    nombre=data["nombre"],
                                    rol=data["rol_id"])
            return usuario_logeado
        except Exception as ex:
            raise Exception(ex)