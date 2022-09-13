class Libro():
    def __init__(self,isbn,titulo,autor,anoedicion,precio,url):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.anoedicion = anoedicion
        self.precio = precio
        self.url = url
        self.unidades_vendidas = 0
