import customtkinter as ctk
from tkinter import ttk
from clase_ingrediente import Ingrediente
from clase_contenedor import Contenedor
from clase_menu import Menu
import re
from CTkMessagebox import CTkMessagebox
from PIL import Image

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Burger Queen")
        self.geometry("1200x700")

        # Inicializar el contenedor de ingredientes
        self.contenedor = Contenedor()

        self.menus_registrados = [crear_menu_papasFritas(), crear_menu_pepsi(), crear_menu_completo(), crear_menu_hamburguesa()]

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()
        

    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de Ingredientes")
        self.tab2 = self.tabview.add("Pedidos")
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


        self.boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", fg_color="black", text_color="white")
        self.boton_generar_menu.configure(command=self.generar_menu)
        self.boton_generar_menu.pack(pady=10)
    
    
        self.boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", fg_color="black", text_color="white")
        self.boton_generar_menu.configure(command=self.generar_menu)
        self.boton_generar_menu.pack(pady=10)
    
    def configurar_pestana2(self):
        frame_treeview2 = ctk.CTkFrame(self.tab2)
        frame_treeview2.pack(fill="both", expand=True, padx=10, pady=10)

        self.tarjetas_frame = ctk.CTkFrame(frame_treeview2)
        self.tarjetas_frame.pack(side="top", fill="x")

        self.tree2 = ttk.Treeview(frame_treeview2, columns=("Nombre del Menu","Cantidad","Precio Unitario"), show="headings")
        self.tree2.heading("Nombre del Menu", text="Nombre del Menu")
        self.tree2.heading("Cantidad", text="Cantidad")
        self.tree2.heading("Precio Unitario", text="Precion Unitario")
        self.tree2.pack(side="bottom", fill="both", padx=10, pady=10)

        
        self.tarjetas_creadas = 0
        for menu in self.menus_registrados:
            self.crear_tarjeta(menu)
            self.tarjetas_creadas += 1

    def crear_tarjeta(self, menu):
        # Obtener el número de columnas y filas actuales
        num_tarjetas = self.tarjetas_creadas
        fila = num_tarjetas // 2
        columna = num_tarjetas % 2
        
        # Crear la tarjeta con un tamaño fijo
        tarjeta = ctk.CTkFrame(self.tarjetas_frame, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15)

        # Hacer que la tarjeta sea completamente clickeable 
        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

        # Cambiar el color del borde cuando el mouse pasa sobre la tarjeta
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        # Verifica si hay una imagen asociada con el menú
        if menu.icono_menu:
            imagen_label = ctk.CTkLabel(tarjeta, image=menu.icono_menu, width=64, height=64, text="", bg_color="transparent")
            imagen_label.pack(anchor="center", pady=5, padx=10)
            imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

            texto_label = ctk.CTkLabel(tarjeta, text=f"{menu.nombre}", text_color="black", font=("Helvetica", 12, "bold"), bg_color="transparent")
            texto_label.pack(anchor="center", pady=1)
            texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        else:
            print(f"No se pudo cargar la imagen para el menú '{menu.nombre}'")
        
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

    def generar_menu(self):      # Este boton debe verificar si hay suficientes ingredientes para crear cada menu
        print("Generando menús...")
        for menu in self.menus_registrados:
            print(menu.nombre)
            for ing_necesario in menu.ingredientes_necesarios:
                print(f"    buscando {ing_necesario.nombre}....")
                if ing_necesario.nombre in self.contenedor.obtener_nombres_ingredientes():
                    print(f"    {ing_necesario.nombre} encontrado")
                    for ing_contenedor in self.contenedor.obtener_ingredientes():
                        if ing_necesario.nombre == ing_contenedor.nombre and ing_necesario.cantidad > ing_contenedor.cantidad:
                            CTkMessagebox(title="Error", message=f"No hay suficiente {ing_necesario.nombre} para crear el menú {menu.nombre}.", icon="warning")
                            break
                else:
                    CTkMessagebox(title="Error", message=f"No hay suficiente {ing_necesario.nombre} para crear el menú {menu.nombre}.", icon="warning")
                    break
            print("--------------------")

    def tarjeta_click(self, event, menu):
        # Verificar si hay suficientes ingredientes en el stock para preparar el menú
        suficiente_stock = True
        if self.contenedor.lista_ingredientes==[]:
            suficiente_stock=False
        for ingrediente_necesario in menu.ingredientes_necesarios:
            for ingrediente_stock in self.contenedor.lista_ingredientes:
                if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                    if int(ingrediente_stock.cantidad) < int(ingrediente_necesario.cantidad):
                        suficiente_stock = False
                        break
            if not suficiente_stock:
                break
        
        if suficiente_stock:
            # Descontar los ingredientes del stock
            for ingrediente_necesario in menu.ingredientes_necesarios:
                for ingrediente_stock in self.contenedor.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad = str(int(ingrediente_stock.cantidad) - int(ingrediente_necesario.cantidad))
            
            # Agregar el menú al pedido
            self.pedido.agregar_menu(menu)
            
            # Actualizar el Treeview
            self.actualizar_treeview_pedido()

            # Actualizar el total del pedido
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            # Mostrar un mensaje indicando que no hay suficientes ingredientes usando CTkMessagebox
            CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")
                            


    
def crear_menu_papasFritas():
    papas = Ingrediente("papas", 5)
    imagen = ctk.CTkImage(light_image=Image.open("imagenes/icono_papas_fritas_64x64.png"), dark_image=Image.open("imagenes/icono_papas_fritas_64x64.png"), size=(64, 64))
    return Menu("Papas Fritas", [papas], 500, imagen)

def crear_menu_pepsi():
    bebida  = Ingrediente("bebida", 1)
    imagen = ctk.CTkImage(light_image=Image.open("imagenes/icono_cola_64x64.png"), dark_image=Image.open("imagenes/icono_cola_64x64.png"), size=(64, 64))
    return Menu("Pepsi", [bebida], 1100, imagen)

def crear_menu_completo():
    vienesa = Ingrediente("vienesa", 1)
    pan_completo = Ingrediente("pan de completo", 1)
    tomate = Ingrediente("tomate", 1)
    palta = Ingrediente("palta", 1)
    imagen = ctk.CTkImage(light_image=Image.open("imagenes/icono_hotdog_sin_texto_64x64.png"), dark_image=Image.open("imagenes/icono_hotdog_sin_texto_64x64.png"), size=(64, 64))
    return Menu("Completo", [vienesa, pan_completo, tomate, palta], 1800, imagen)

def crear_menu_hamburguesa():
    pan_hamburguesa = Ingrediente("pan de hamburguesa", 1)
    queso = Ingrediente("lamina de queso", 1)
    churrasco = Ingrediente("churrasco de carne", 1)
    imagen = ctk.CTkImage(light_image=Image.open("imagenes/icono_hamburguesa_negra_64x64.png"), dark_image=Image.open("imagenes/icono_hamburguesa_negra_64x64.png"), size=(64, 64))
    return Menu("Hamburguesa", [pan_hamburguesa, queso, churrasco], 3500, imagen)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

  

    app = AplicacionConPestanas()
    app.mainloop()
