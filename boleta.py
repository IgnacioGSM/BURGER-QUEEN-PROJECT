from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Boleta Restaurante', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Gracias por su compra. Para cualquier consulta, llámenos al +56 9 1234 5678', 0, 1, 'C')
        self.cell(0, 10, 'Los productos adquiridos no tienen garantía', 0, 0, 'C')

# Datos del restaurante (fijos)
datos_restaurante = {
    'Razon Social': 'Razón Social del Negocio',
    'RUT': '12345678-9',
    'Direccion': 'Calle Falsa 123',
    'Telefono': '+56 9 1234 5678',
    'Fecha': '22/08/2024 16:46:12',
}

# Productos (precios unitarios son fijos)
productos = [
    {'nombre': 'Papas Fritas', 'precio_unitario': 500},
    {'nombre': 'Completo', 'precio_unitario': 1800},
    {'nombre': 'Pepsi', 'precio_unitario': 1100},
    {'nombre': 'Hamburguesa', 'precio_unitario': 3500},
]

# Cantidades ingresadas por el usuario
cantidades = [2, 2, 3, 2]  # Estas cantidades pueden ser ingresadas dinámicamente según lo requieras

# Crear PDF
pdf = PDF()
pdf.add_page()

# Información del restaurante
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, f"RUT: {datos_restaurante['RUT']}", 0, 1)
pdf.cell(0, 10, f"Dirección: {datos_restaurante['Direccion']}", 0, 1)
pdf.cell(0, 10, f"Teléfono: {datos_restaurante['Telefono']}", 0, 1)
pdf.cell(0, 10, f"Fecha: {datos_restaurante['Fecha']}", 0, 1)

# Espacio antes de la tabla
pdf.ln(10)

# Encabezado de la tabla
pdf.set_font('Arial', 'B', 12)
pdf.cell(50, 10, 'Nombre', 1)
pdf.cell(30, 10, 'Cantidad', 1)
pdf.cell(40, 10, 'Precio Unitario', 1)
pdf.cell(40, 10, 'Subtotal', 1)
pdf.ln()

# Cálculo de totales
subtotal = 0

# Añadir productos a la tabla
pdf.set_font('Arial', '', 12)
for i, producto in enumerate(productos):
    cantidad = cantidades[i]
    precio_unitario = producto['precio_unitario']
    subtotal_producto = cantidad * precio_unitario
    subtotal += subtotal_producto
    
    pdf.cell(50, 10, producto['nombre'], 1)
    pdf.cell(30, 10, str(cantidad), 1)
    pdf.cell(40, 10, f"${precio_unitario:.2f}", 1)
    pdf.cell(40, 10, f"${subtotal_producto:.2f}", 1)
    pdf.ln()

# Cálculo del IVA y total
iva = subtotal * 0.19
total = subtotal + iva

# Espacio antes de los totales
pdf.ln(5)

# Subtotal, IVA y Total
pdf.cell(0, 10, f"Subtotal: ${subtotal:.2f}", 0, 1, 'R')
pdf.cell(0, 10, f"IVA (19%): ${iva:.2f}", 0, 1, 'R')
pdf.cell(0, 10, f"Total: ${total:.2f}", 0, 1, 'R')

# Guardar PDF
pdf.output("boleta_restaurante.pdf")

print("PDF generado: boleta_restaurante.pdf")
    