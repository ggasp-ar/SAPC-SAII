from xml.dom import NoModificationAllowedErr
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(UserMixin):
    def __init__(self, id, usuario, nombre, rol, password):
        self.id = id #User ID
        self.usuario = usuario #Username
        self.nombre = nombre #Full Name
        self.password = password #Only used to create a new user
        self.rol = rol #Admin, User, etc..

    @classmethod
    def verificar_password(self,encriptado ,password):
        return check_password_hash(encriptado, password)
    
    @classmethod
    def crear_password(self,password):
        return generate_password_hash(password)
    
    @property
    def info(self):
        return {'nombre':self.nombre,
                'rol':self.rol,
                }