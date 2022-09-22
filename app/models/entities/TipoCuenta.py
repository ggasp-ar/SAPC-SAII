class TipoCuenta():

    def __init__(self, id, tipo, descripcion):
        self.id = id #tipo_id
        self.tipo = tipo
        self.descripcion = descripcion

    def getTipo(self):
        return self.tipo

    def getDescripcion(self):
        return self.descripcion
          
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