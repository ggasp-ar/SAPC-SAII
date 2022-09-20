
class Cuenta():

    def __init__(self, id, codigo, nombre, saldo, tipo, recibe, padreid):
        self.id = id #Cuenta ID
        self.codigo = codigo
        self.nombre = nombre #Nombre de cuenta
        self.saldo = saldo
        self.tipo = tipo
        self.recibe_saldo = recibe
        self.padreid = padreid
        self.padre = None
        self.hijos = []

    def agregarHijo(self, cuenta):
        self.hijos.append(cuenta)
        
    def eliminarHijo(self, cuenta):
        self.hijos.remove(cuenta)
    
    def getHijos(self):
        return self.hijos

    def getId(self):
        return self.id
        
    def getCodigo(self):
        return self.codigo

    def getNombre(self):
        return self.nombre

    def setPadre(self, cuenta):
        self.padre = Cuenta
    
    def getPadreId(self):
        return self.padreid

    
    def getSaldo(self):
        return self.saldo
    
    def getTipo(self):
        return self.tipo
    
    def getRecibe(self):
        if (self.hijos == []):
            return True
        else:
            return False
   
    def __repr__(self):
        attrs = self.id,self.codigo,self.nombre,self.tipo,self.saldo,self.padre,self.hijos
        stratr = []
        for a in attrs:
            stratr.append(str(a))            
        return "::".join((stratr))