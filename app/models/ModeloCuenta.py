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
                    recibe = bool(data["recibe_saldo"]),
                    saldo = data["saldo_actual"],
                    tipo = self.Tipos[data["tipo_id"]],
                    padreid = data["cuenta_padre_id"])
        return acc
    
    @classmethod
    def obtenerPor(self,db,campo,valor, byCodigo):
        self.cargarTipos(db)
        try:
            sql = """SELECT *
                    FROM CUENTAS c
                    WHERE c.{0} = {1} """.format(campo,valor)      
            data = fetchAll(db,sql)
            if data != None:
                cuentas={}
                for c in data:
                    cuenta = self.generarCuenta(c)
                    index = (cuenta.getCodigo() if byCodigo else cuenta.getId())
                    cuentas[index] = cuenta 
            else:
                cuentas = None
            return cuentas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtenerCuentas(self,db):
        self.cargarTipos(db)
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
            'text':cta.getNombre(),
            'tags':[(' ({})'.format(cta.getTipo().getTipo()))]
        }
        hijos=cta.getHijos()
        if hijos != []:
            d['nodes']=[]
            for h in hijos:
                d['nodes'].append(self.cuentaToDict(h))
        if d['recibe']:
            d['backColor'] = " #EEEEEE"
        else:
            d['backColor'] = " #FFFFFF"
        return d
    
    @classmethod
    def cuentaToDictSimplificado(self,cta):
        d={
            'cid':cta.getId(),
            'codigo':cta.getCodigo(),
            'saldo':cta.getSaldo(),
            'tipo':cta.getTipo().toDict(),
            'text':cta.getNombre(),
            'tags':[(' ({})'.format(cta.getTipo().getTipo()))]
        }
        return d
    
    @classmethod
    def generarArbol(self,db):
        fam = self.generarFamilia(db)
        tree = []
        for p in fam:
            tree.append(self.cuentaToDict(p))
        return tree

    @classmethod
    def obtenerCuentasSaldo(self,db, byCodigo=True):
        acc = self.obtenerPor(db, "recibe_saldo","1", byCodigo)
        return acc
        
    @classmethod
    def obtenerDict(self,cuentas,simplificado=False):
        accs = []
        for c in cuentas:
            if simplificado:
                accs.append(self.cuentaToDictSimplificado(cuentas[c]))
            else:
                accs.append(self.cuentaToDict(cuentas[c]))
        return accs

    @classmethod
    def actualizarCuenta(self, db, cuenta):
        cursor = db.connection.cursor()
        cursor.execute("UPDATE cuentas SET saldo_actual = %s WHERE cuenta_id = %s;",
            (cuenta.getSaldo(),cuenta.getId()))
    
    @classmethod
    def actualizarCuentas(self, db, cuentas):
        for c in cuentas:
            self.actualizarCuenta(db, cuentas[c])
        return True
    
    @classmethod
    def verificarCuenta(self,cuenta):
        #cuenta.getNombre()
        return True

    @classmethod
    def cargarNuevaCuenta(self, db, cuenta):
        if(self.verificarCuenta(cuenta)):
            cursor = db.connection.cursor()
            pid = cuenta.getPadreId()
            padre = self.obtenerPor(db, 'cuenta_id', pid, False)[pid]
            print(padre)
            cursor.execute("INSERT INTO cuentas (cuenta, cuenta_padre_id, codigo, tipo_id, recibe_saldo) VALUES (%s, %s, %s, %s, %s)",
            (cuenta.getNombre(),
            padre.getCodigo(),
            cuenta.getCodigo(),
            padre.getTipo().getTipoId(),
            cuenta.getRecibe()))
            db.connection.commit()




