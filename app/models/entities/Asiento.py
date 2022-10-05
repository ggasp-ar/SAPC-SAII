
class Asiento():

    def __init__(self, id, fecha, desc, usuario_id, asientos):
        self.id = id
        self.fecha = (fecha.replace('T',' ') + ':00')
        self.desc = desc
        self.responsable = usuario_id
        self.asientos_cuentas = asientos

    def getId(self):
      return self.id

    def getFecha(self):
      return self.fecha

    def getDesc(self):
      return self.desc

    def getResponsable(self):
      return self.responsable

    def getAsientos(self):
      return self.asientos_cuentas
