from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(UserMixin):
    def __init__(self, id, usuario, password,tipousuario, celular):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.tipousuario = tipousuario
        self.celular = celular

    @classmethod
    def verificar_password(self,encriptado ,password):
        return check_password_hash(encriptado, password)
    
    @classmethod
    def crear_password(self,password):
        return generate_password_hash(password)