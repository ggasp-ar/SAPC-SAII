

from datetime import date
from xml.etree.ElementTree import tostring
from app.models.entities.Asiento import Asiento
from app.models.entities.Cuenta import Cuenta
from app.utils import debugPrint, fetchAll, fetchOne


class ModeloAsiento():

    @classmethod
    def crearAsiento(self, raw_asiento):
      transacciones=[]
      a = raw_asiento['asientos']
      for t in a:
        if a[t] != None:
          transacciones.append(a[t])
      return Asiento(id=raw_asiento['id'],
          fecha=raw_asiento['fecha'], 
          desc=raw_asiento['descripcion'], 
          usuario_id=raw_asiento['responsableid'], 
          asientos=transacciones)

    @classmethod
    def cargarAsiento(self, db, asiento, cuentasModificadas):
      cursor = db.connection.cursor()
      cursor.execute("INSERT INTO asientos (fecha, descripcion, usuario_id) VALUES (%s, %s, %s)",
        (asiento.getFecha(),
         asiento.getDesc(), 
        asiento.getResponsable()))
      
      aid= cursor.lastrowid
      type(asiento.getAsientos())
      
      i=0
      for tr in asiento.getAsientos():
        sql = 'INSERT INTO asientos_cuentas (asiento_id, cuenta_id, orden, valor, saldo, haber) VALUES (%s, %s, %s,%s, %s, %s)'
        cid = int(tr['cuenta_id'])
        values = (aid, cid , i, tr['monto'], cuentasModificadas[cid].getSaldo(), int(tr['haber']))
        cursor.execute(sql,values)
        i = i+1

    @classmethod
    def verificarAsiento(self, asiento, cuentas, noDupes=True):
      cuentas_usadas = {}
      asientos = asiento.getAsientos()
      if len(asientos) <2:
        raise Exception('Asiento Invalido')
      for tr in asiento.getAsientos():
        cid   = int(tr['cuenta_id'])
        monto = float(tr['monto'])
        haber = bool(tr['haber'])
        
        if cid not in cuentas.keys():
          raise Exception('error con la cuenta' + tr['cuenta'] + ' "id:' + str(cid) + '". No recibe saldo.')
        
        if (cid in cuentas_usadas.keys()) and noDupes:
          raise Exception('error con la cuenta ' + tr['cuenta'] + '  "id:' + str(cid) + '". Ya se encuentra registrada en otra transaccion.')
        cuenta = cuentas[cid]
        cuenta.transaccion(monto,haber)
        cuentas_usadas[cid] = cuenta
      return asiento,cuentas_usadas

    @classmethod
    def nextAsientoId(self,db):
      try:
        id = fetchOne(db, 'SELECT COUNT(asiento_id) AS C FROM asientos')['C']
        return (id + 1)
      except:
        return (0)

    @classmethod
    def generarAsiento(self, data, transacciones_raw):
      transacciones=[]
      for t in transacciones_raw:
        transacciones.append([
          t['cuenta'],t['valor'],t['haber']
        ])
      a = Asiento(id = data['asiento_id'], 
                  fecha = str(data['fecha']).replace(' ','T'), 
                  desc = data['descripcion'], 
                  usuario_id = data['usuario_id'],
                  asientos = transacciones)
      return a

    @classmethod
    def obtenerAsiento(self, db, id):
        try:
            sql = """SELECT *
                    FROM ASIENTOS a
                    WHERE a.asiento_id = {0} """.format(id) 
            sql_ac = """SELECT *
                    FROM asientos_cuentas a INNER JOIN cuentas c ON (a.cuenta_id = c.cuenta_id)
                    WHERE a.asiento_id = {0} """.format(id)        
            data = fetchOne(db, sql)
            data_tr = fetchAll(db, sql_ac)
            if data != None:
              debugPrint(data, "obtenerAsiento")
              debugPrint(data_tr, "obtenerAsiento")
              asiento = self.generarAsiento(data, data_tr)
            else:
              asiento = None
            return asiento
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def listarAsientos(self, db, desde, hasta, ascendente):
        try:
            orden = 'ASC' if ascendente else 'DESC'
            sql = """SELECT *
                    FROM ASIENTOS a
                    WHERE a.fecha >= '{0}' AND a.fecha <= '{1} 23:59:59' 
                    ORDER BY a.fecha {2}""".format(desde, hasta, orden) 
            data = fetchAll(db, sql)
            asientos = []
            if data != None:
              for a in data:
                asientos.append(
                  Asiento(
                    id = a['asiento_id'], 
                    fecha = str(a['fecha']).replace(' ','T'), 
                    desc = a['descripcion'], 
                    usuario_id = a['usuario_id'],
                    asientos = [])
                )
            else:
              asientos = None
            return asientos
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def inicioActividades(self, db):
      try:
        sql = """SELECT MIN(fecha) fecha FROM asientos"""
        data = fetchOne(db, sql)
        if data == None:
          return ''
        fecha = data['fecha'].isoformat(sep='T',timespec='auto')
        return fecha.split('T')
      except Exception as ex:
          raise Exception(ex)
            