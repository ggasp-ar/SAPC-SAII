
class Cuenta():

    def __init__(self, id, codigo, nombre, saldo, tipo, recibe, padreid, habilitada):
        self.id = id #Cuenta ID
        self.codigo = codigo
        self.nombre = nombre #Nombre de cuenta
        self.saldo = saldo
        self.tipo = tipo
        self.recibe_saldo = recibe
        self.padreid = padreid
        self.padre = None
        self.hijos = []
        self.habilitada = habilitada

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
    
    def setCodigo(self, codigo):
        self.codigo = codigo
    
    def getHabilitada(self):
        return self.habilitada

    def getSaldo(self):
        saldo = 0
        if( self.hijos != []):
            for hijo in self.hijos:
                saldo = saldo + hijo.getSaldo()
            return saldo
        return self.saldo
    
    def setSaldo(self,nuevoSaldo):
        self.saldo = nuevoSaldo
        return nuevoSaldo
    
    def getTipo(self):
        return self.tipo
    
    def getRecibe(self):
        return self.recibe_saldo
   
    def transaccion(self, monto, haber):
        nuevoMonto = self.getSaldo() + self.getTipo().transaccion(monto,haber)
        if nuevoMonto < 0:
            err = "La cuenta " + self.nombre + " no tiene suficiente saldo para realizar la transaccion."
            raise Exception(err)
        self.setSaldo(nuevoMonto)
        print("Transaccion:", nuevoMonto, "a la cuenta", self.nombre, "  Nuevo Saldo:", self.getSaldo())
        return True

    def __repr__(self):
        attrs = self.id,self.codigo,self.nombre,self.tipo,self.saldo,self.padre,self.hijos
        stratr = []
        for a in attrs:
            stratr.append(str(a))            
        return "::".join((stratr))