class Contenedor:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        for ing in self.lista_ingredientes:
            if ing.nombre == ingrediente.nombre:
                return False    # ingrediente ya existe en la lista
        self.lista_ingredientes.append(ingrediente)
        return True  # ingrediente agregado como nuevo

    def eliminar_ingrediente(self, nombre_ingrediente, cantidad=1):
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre_ingrediente:
                for i in range(cantidad):
                    self.lista_ingredientes.remove(ing)
                return True
        else: 
            return False



    def obtener_ingredientes(self):
        return [ing for ing in self.lista_ingredientes]
