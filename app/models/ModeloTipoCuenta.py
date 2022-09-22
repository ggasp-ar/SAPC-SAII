from pydoc import describe

from app.models.entities.TipoCuenta import TipoCuenta
from app.utils import fetchAll, fetchOne


class ModeloTipoCuenta():

    @classmethod
    def crearTipo(self, data):
        tipo = TipoCuenta(id = data["tipo_id"], 
                        tipo = data["tipo"], 
                        descripcion = data["descripcion"],)
        return tipo
    
    @classmethod
    def obtenerTipos(self,db):
        sql = """SELECT *
                 FROM TIPOS t"""
        tipos_raw = fetchAll(db,sql)
        tipos={}
        for t in tipos_raw:
            tipo = self.crearTipo(t)
            tipos[t["tipo_id"]]=tipo
        return tipos
        
    @classmethod
    def obtenerTipo(self,db,id):
        sql = """SELECT *
                 FROM TIPOS t
                 WHERE tipo_id = {0}""".format(id)
        tipo_raw = fetchOne(db,sql)
        return self.crearTipo(tipo_raw)

    