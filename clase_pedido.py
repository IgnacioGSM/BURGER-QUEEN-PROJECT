class Pedido:
    def __init__(self):
        self.menus = []

    def agregar_menu(self, menu):
        self.menus.append(menu)

    def calcular_total(self):
        return sum(menu.precio for menu in self.menus)