from app.models.ModeloTipoCuenta import ModeloTipoCuenta
from .entities.Cuenta import Cuenta
from .entities.TipoCuenta import TipoCuenta
from ..utils import debugPrint, fetchAll, fetchOne

class ModeloCuenta():
    def __init__(self):
        self.Tipos={}

    @classmethod
    def cargarTipos(self, db):
        self.Tipos=ModeloTipoCuenta().obtenerTipos(db)
        return self.Tipos

    @classmethod
    def generarCuenta(self, data):
        acc = Cuenta(id = data["cuenta_id"], 
                    nombre = data["cuenta"], 
                    codigo = data["codigo"],
                    recibe = data["recibe_saldo"],
                    saldo = data["saldo_actual"],
                    tipo = self.Tipos[data["tipo_id"]],
                    padreid = data["cuenta_padre_id"])
        return acc

    @classmethod
    def obtenerPor(self,db,campo,valor):
        self.cargarTipos(db)
        debugPrint()
        try:
            sql = """SELECT *
                    FROM CUENTAS c
                    WHERE c.{0} = {1} """.format(campo,valor)      
            data = fetchAll(db,sql)
            if data != None:
                cuentas=[]
                for c in data:
                    cuentas.append(self.generarCuenta(c)) 
            else:
                cuentas = None
            return cuentas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtenerCuentas(self,db):
        debugPrint(self.cargarTipos(db),"ObtenerCUentas")

        sql = """SELECT *
                 FROM CUENTAS c"""
        allAccs = fetchAll(db,sql)
        accs={}
        for c in allAccs:
            cuenta = self.generarCuenta(c)
            accs[cuenta.getCodigo()]=cuenta
        return accs
            
    @classmethod
    def generarFamilia(self,db):
        allAccs=self.obtenerCuentas(db)
        raices=[]
        for ccod in allAccs:
            c = allAccs[ccod]
            pid = c.getPadreId()
            if pid == None:
                raices.append(c)
            else:
                allAccs[pid].agregarHijo(c)
                c.setPadre(allAccs[pid])
        return raices

    @classmethod
    def cuentaToDict(self,cta):

        d={
            'cid':cta.getId(),
            'codigo':cta.getCodigo(),
            'saldo':cta.getSaldo(),
            'tipo':cta.getTipo().toDict(),
            'recibe':cta.getRecibe(),
            'text':cta.getNombre()
        }
        hijos=cta.getHijos()
        if hijos != []:
            d['nodes']=[]
            for h in hijos:
                d['nodes'].append(self.cuentaToDict(h))
        return d

    @classmethod
    def generarArbol(self,db):
        fam = self.generarFamilia(db)
        tree = []
        for p in fam:
            tree.append(self.cuentaToDict(p))
        return tree


