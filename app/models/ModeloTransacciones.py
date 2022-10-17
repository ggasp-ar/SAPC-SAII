

from ctypes import Array
from datetime import date
from xml.etree.ElementTree import tostring

from flask import jsonify
from app.models.entities.Asiento import Asiento
from app.models.entities.Cuenta import Cuenta
from app.utils import debugPrint, fetchAll, fetchOne


class ModeloTransacciones():
    
    @classmethod
    def listarTransaccionesCuenta(self, db, cuenta, desde, hasta, ascendente = True):
        try:
            orden = 'ASC' if ascendente else 'DESC'
            sql = """SELECT fecha, a.asiento_id, a.descripcion, ac.valor, ac.haber, ac.saldo
                    FROM (asientos a INNER JOIN asientos_cuentas ac ON (a.asiento_id = ac.asiento_id)) INNER JOIN cuentas c ON (ac.cuenta_id = c.cuenta_id)
                    WHERE a.fecha >= '{0}' AND a.fecha <= '{1} 23:59:59' AND c.cuenta_id = {2}
                    ORDER BY a.fecha {3}""".format(desde, hasta, cuenta,orden) 
            data = fetchAll(db, sql)
            transacciones = {}
            if data != None:
              for a in data:
                fechaString = a['fecha'].isoformat(sep=' ',timespec='auto')
                transacciones[fechaString]={
                  'Desc': a['descripcion'],
                  'Valor': float(a['valor']),
                  'Haber': bool(a['haber']),
                  'SaldoParcial': float(a['saldo']),
                  'Asiento': int(a['asiento_id'])
                  }
            else:
              transacciones = None
            return transacciones
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def listarTransacciones(self, db, desde, hasta, ascendente = True):
        try:
            orden = 'ASC' if ascendente else 'DESC'
            sql = """SELECT fecha, a.asiento_id, c.cuenta, ac.valor, ac.haber
                    FROM (asientos a INNER JOIN asientos_cuentas ac ON (a.asiento_id = ac.asiento_id)) INNER JOIN cuentas c ON (ac.cuenta_id = c.cuenta_id)
                    WHERE a.fecha >= '{0}' AND a.fecha <= '{1} 23:59:59' 
                    ORDER BY a.fecha {2}""".format(desde, hasta, orden) 
            data = fetchAll(db, sql)
            transacciones = {}
            if data != None:
              for a in data:
                fechaString = a['fecha'].isoformat(sep=' ',timespec='auto')
                try:
                  t = transacciones[fechaString]
                  t.append({
                    'Cuenta': a['cuenta'],
                    'Valor': float(a['valor']),
                    'Haber': bool(a['haber']),
                    'Asiento': int(a['asiento_id'])
                    })
                except:
                  transacciones[fechaString]=[{
                    'Cuenta': a['cuenta'],
                    'Valor': float(a['valor']),
                    'Haber': bool(a['haber']),
                    'Asiento': int(a['asiento_id'])
                    }]
            else:
              transacciones = None
            return transacciones
        except Exception as ex:
            raise Exception(ex)
            