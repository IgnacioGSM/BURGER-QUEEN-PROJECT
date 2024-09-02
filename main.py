import customtkinter as ctk
from tkinter import ttk
from clase_ingrediente import Ingrediente
from clase_contenedor import Contenedor
import re
from CTkMessagebox import CTkMessagebox

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Burger Queen")
        self.geometry("1200x700")

        # Inicializar el contenedor de ingredientes
        self.contenedor = Contenedor()

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()
        

    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de Ingredientes")
        self.tab2 = self.tabview.add("Pedidos ya")
        # Configurar el contenido de la pestaña 1
        self.configurar_pestana1()
        self.configurar_pestana2()

    def configurar_pestana1(self):
        # Dividir la pestaña en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_nombre = ctk.CTkLabel(frame_formulario, text="Cantidad del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        #Boton de ingreso
        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Registrar ingrediente")
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        # Botón para eliminar ingredienternegna arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar ingrediente", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre","Cantidad"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def configurar_pestana2(self):
        label = ctk.CTkLabel(self.tab2,text="hola mundo")
        label.pack(pady=20)

    def validar_texto(self, texto, message="El nombre debe contener solo letras y espacios."):
        if re.match(r"^[a-zA-Z\s]+$", texto):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message=message, icon="warning")
            return False
    
    def validar_int_positivo(self, presunto_numero):
        try: int(presunto_numero)
        except: 
            CTkMessagebox(title="Error de Validación", message="Ingrese un numero entero para la cantidad.", icon="warning")
            return False
        else:
            if int(presunto_numero) <= 0:
                CTkMessagebox(title="Error",message="El numero debe ser mayor a 0", icon="warning")
                return False
            else:
                return True

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()

        # Validar entradas
        if not self.validar_texto(nombre):
            return
        if not self.validar_int_positivo(cantidad):
            return
        
        # Crear una instancia de ingrediente
        ingrediente = Ingrediente(nombre,cantidad)

        # Agregar el ingrediente al contenedor
        if self.contenedor.agregar_ingrediente(ingrediente):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El ingrediente ya está registrado.", icon="warning")

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]
        #cantidad = item['values'][1]       por ahora no se necesita sacar la cantidad
        
        # Eliminar el ingrediente del contenedor
        if self.contenedor.eliminar_ingrediente(nombre):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El ingrediente no se pudo eliminar.", icon="warning")

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar todos los ingredientes del conteenedor al Treeview
        for ingrediente in self.contenedor.obtener_ingredientes():
            self.tree.insert("", "end", values=(ingrediente.nombre,ingrediente.cantidad))


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionConPestanas()
    app.mainloop()
