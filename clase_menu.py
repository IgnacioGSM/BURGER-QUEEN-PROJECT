from clase_ingrediente import Ingrediente

class Menu:
    def __init__(self, nombre, ingredientes:list[Ingrediente], precio_unitario):
        self.nombre = nombre
        self.ingredientes_necesarios = ingredientes
        self.precio_unitario = precio_unitario

# Al crear un Menú, se le asigna un nombre, una lista de ingredientes necesarios y un precio unitario.
# La lista de ingredientes necesarios es una lista de objetos de la clase Ingrediente.
# Por lo que para crear un objeto de la clase Menú se necesita tener creados objetos de clase ingrediente
# Estos no estarán guardados en el contenedor, se usarán de modelo para crear el menú

# En el main se crearán los objetos de la clase Ingrediente y se pasarán como argumento 
# para crear un objeto de la clase Menú