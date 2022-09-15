from xml.dom import NoModificationAllowedErr
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(UserMixin):
    def __init__(self, id, usuario, nombre, password, rol, email=None):
        self.id = id
        self.usuario = usuario
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.email = email

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
                'email':self.email}