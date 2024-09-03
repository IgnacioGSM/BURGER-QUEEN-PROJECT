class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = int(cantidad)

    def __str__(self):
        return f"{self.nombre}, {self.cantidad}"
