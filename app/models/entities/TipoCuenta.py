from operator import truediv
import re


class TipoCuenta():

    def __init__(self, id, tipo, descripcion):
        self.id = id #tipo_id
        self.tipo = tipo
        self.descripcion = descripcion

    def getTipo(self):
        return self.tipo

    def getDescripcion(self):
        return self.descripcion

    def transaccion(self,monto,haber):
        if self.tipo in ("Ac","Pa","Pm"):
            if (self.tipo == "Ac"):
                return (-monto) if haber else (monto)
            else:
                return (monto) if haber else (-monto)
        elif self.tipo in ("R+","R-"):
            if (self.tipo == "R+" and not(haber)):
                raise Exception("Resultado positivo en el debe")
            
            if (self.tipo == "R-" and haber):
                raise Exception("Resultado Negativo en el haber")

            return monto
        else:
            raise Exception("Server Error: Tipo de Cuenta Invalido")
          
    def __repr__(self):
            attrs = self.id,self.tipo,self.descripcion
            stratr = []
            for a in attrs:
                stratr.append(str(a))            
            return "::".join((stratr))

    def toDict(self):
        return {
                'id': self.id,
                'tipo': self.tipo,
                'descripcion': self.descripcion
                }