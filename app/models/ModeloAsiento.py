

from datetime import date
from xml.etree.ElementTree import tostring
from app.models.entities.Asiento import Asiento
from app.utils import debugPrint, fetchOne


class ModeloAsiento():

    @classmethod
    def crearAsiento(self, raw_asiento):
      return Asiento(id=raw_asiento['id'],
          fecha=raw_asiento['fecha'], 
          desc=raw_asiento['descripcion'], 
          usuario_id=raw_asiento['responsableid'], 
          asientos=raw_asiento['asientos'])

    @classmethod
    def cargarAsiento(self, db, asiento):
      cursor = db.connection.cursor()
      cursor.execute("INSERT INTO asientos (fecha, descripcion, usuario_id) VALUES (%s, %s, %s)",
        (asiento.getFecha(),
         asiento.getDesc(), 
        asiento.getResponsable()))
      
      aid= cursor.lastrowid
      type(asiento.getAsientos())
      debugPrint(asiento.getAsientos(), 'cargaAsiento() para el asiento {}'.format(aid))
      
      i=0
      for a in asiento.getAsientos():
        sql = 'INSERT INTO asientos_cuentas (asiento_id, cuenta_id, orden, valor, saldo, haber) VALUES (%s, %s, %s,%s, %s, %s)'
        values = (aid, int(a['cuenta_id']), i, a['monto'], 0, int(a['haber']))
        debugPrint("SQL" + sql, "Insertando Asiento")
        debugPrint(values, "Insertando Asiento" )
        cursor.execute(sql,values)
        i = i+1
      
      db.connection.commit()

    def nextAsientoId(self,db):
      try:
        id = fetchOne(db, 'SELECT MAX(asiento_id) id FROM asientos')['id']
        return (id + 1)
      except:
        return (0)