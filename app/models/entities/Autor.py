class Autor():
    def __init__(self, id,nombres,apellidos,fechanacimiento=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.fechanacimiento = fechanacimiento

    def nombre_completo(self):
        return "{}, {}".format(self.nombres, self.apellidos)