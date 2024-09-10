class Contenedor:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        for i in range(len(self.lista_ingredientes)):
            if self.lista_ingredientes[i].nombre == ingrediente.nombre:
                self.lista_ingredientes[i].cantidad += ingrediente.cantidad
                return True
                
        self.lista_ingredientes.append(ingrediente)
        return True  # ingrediente agregado como nuevo

    def eliminar_ingrediente(self, nombre_ingrediente, cantidad=1):
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre_ingrediente:
                if ing.cantidad >= cantidad:
                    ing.cantidad -= cantidad
                    if ing.cantidad == 0:
                        self.lista_ingredientes.remove(ing)
                    return True
                else:
                    return False
        else: 
            return False

    def obtener_ingredientes(self):
        return [ing for ing in self.lista_ingredientes]

    def obtener_nombres_ingredientes(self):
        return [ing.nombre for ing in self.lista_ingredientes]