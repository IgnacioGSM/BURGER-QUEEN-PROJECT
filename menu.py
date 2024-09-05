import tkinter as tk
from tkinter import ttk, messagebox

class Ingrediente:
    def __init__(self, nombre, cantidad_disponible):
        self.nombre = nombre
        self.cantidad_disponible = cantidad_disponible

class Menu:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Ingredientes y Menús")
        self.root.geometry("600x400")  # Tamaño de ventana ajustado
        
        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Pestaña de ingredientes
        self.tab_ingredientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ingredientes, text="Ingredientes")
        
        # Treeview para mostrar los ingredientes
        self.tree_ingredientes = ttk.Treeview(self.tab_ingredientes, columns=("Nombre", "Cantidad"), show="headings")
        self.tree_ingredientes.heading("Nombre", text="Nombre")
        self.tree_ingredientes.heading("Cantidad", text="Cantidad")
        self.tree_ingredientes.pack(pady=10, fill="x")
        
        # Entradas y botones
        self.form_frame = ttk.Frame(self.tab_ingredientes)
        self.form_frame.pack(pady=10, fill="x")
        
        ttk.Label(self.form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.form_frame)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(self.form_frame)
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.form_frame, text="Ingresar Ingrediente", command=self.agregar_ingrediente).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.form_frame, text="Eliminar Ingrediente", command=self.eliminar_ingrediente).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.form_frame, text="Generar Menú", command=self.generar_menu).grid(row=2, column=2, padx=5, pady=5)
        
        # Pestaña de pedidos
        self.tab_pedidos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pedidos, text="Pedidos")

        # Treeview para mostrar los menús
        self.tree_menus = ttk.Treeview(self.tab_pedidos, columns=("Nombre", "Precio"), show="headings")
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.heading("Precio", text="Precio")
        self.tree_menus.pack(pady=10, fill="x")

        # Botones para agregar menús
        self.menu_buttons_frame = ttk.Frame(self.tab_pedidos)
        self.menu_buttons_frame.pack(pady=10)

        ttk.Button(self.menu_buttons_frame, text="Agregar Papas Fritas", command=lambda: self.agregar_menu("Papas Fritas")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.menu_buttons_frame, text="Agregar Pepsi", command=lambda: self.agregar_menu("Pepsi")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.menu_buttons_frame, text="Agregar Completo", command=lambda: self.agregar_menu("Completo")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.menu_buttons_frame, text="Agregar Hamburguesa", command=lambda: self.agregar_menu("Hamburguesa")).grid(row=0, column=3, padx=5, pady=5)

        # Botón para eliminar menú
        ttk.Button(self.tab_pedidos, text="Eliminar Menú", command=self.eliminar_menu).pack(pady=10)
        
        # Etiqueta para mostrar el total
        self.label_total = ttk.Label(self.tab_pedidos, text="Total: $0.00")
        self.label_total.pack(pady=10)

        # Contenedores de ingredientes y menús
        self.stock = []
        self.pedidos = []

        # Precios fijos para los menús
        self.precios_menus = {
            "Papas Fritas": 500,
            "Pepsi": 1100,
            "Completo": 1800,
            "Hamburguesa": 3500
        }

        self.actualizar_treeview_ingredientes()

    def agregar_ingrediente(self):
        nombre = self.entry_nombre.get().strip()
        cantidad_str = self.entry_cantidad.get().strip()

        if not nombre or not cantidad_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un valor positivo.")
            return

        for ing in self.stock:
            if ing.nombre == nombre:
                ing.cantidad_disponible += cantidad
                self.actualizar_treeview_ingredientes()
                messagebox.showinfo("Actualizado", f"Cantidad de '{nombre}' actualizada.")
                return

        nuevo_ingrediente = Ingrediente(nombre, cantidad)
        self.stock.append(nuevo_ingrediente)
        self.actualizar_treeview_ingredientes()
        messagebox.showinfo("Agregado", f"Ingrediente '{nombre}' agregado con éxito.")

    def eliminar_ingrediente(self):
        selected_item = self.tree_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un ingrediente para eliminar.")
            return

        nombre = self.tree_ingredientes.item(selected_item[0])["values"][0]
        self.stock = [ing for ing in self.stock if ing.nombre != nombre]
        self.actualizar_treeview_ingredientes()
        messagebox.showinfo("Eliminado", f"Ingrediente '{nombre}' eliminado con éxito.")

    def generar_menu(self):
        self.tree_menus.delete(*self.tree_menus.get_children())
        for nombre, precio in self.precios_menus.items():
            self.tree_menus.insert("", "end", values=(nombre, f"${precio:.2f}"))

    def agregar_menu(self, nombre):
        if nombre in self.precios_menus:
            precio = self.precios_menus[nombre]
            self.pedidos.append(Menu(nombre, precio))
            self.actualizar_treeview_menus()
            self.actualizar_total()
        else:
            messagebox.showwarning("Advertencia", "El menú seleccionado no está disponible.")

    def eliminar_menu(self):
        selected_item = self.tree_menus.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un menú para eliminar.")
            return

        nombre = self.tree_menus.item(selected_item[0])["values"][0]
        self.pedidos = [menu for menu in self.pedidos if menu.nombre != nombre]
        self.actualizar_treeview_menus()
        self.actualizar_total()
        messagebox.showinfo("Eliminado", f"Menú '{nombre}' eliminado con éxito.")

    def actualizar_treeview_ingredientes(self):
        for item in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(item)
        for ing in self.stock:
            self.tree_ingredientes.insert("", "end", values=(ing.nombre, ing.cantidad_disponible))

    def actualizar_treeview_menus(self):
        for item in self.tree_menus.get_children():
            self.tree_menus.delete(item)
        for menu in self.pedidos:
            self.tree_menus.insert("", "end", values=(menu.nombre, f"${menu.precio:.2f}"))

    def actualizar_total(self):
        total = sum(menu.precio for menu in self.pedidos)
        self.label_total.config(text=f"Total: ${total:.2f}")

# Crear la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()
