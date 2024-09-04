from fpdf import FPDF 


# Crear un objeto PDF
pdf = FPDF()


# Agregar una pagina
pdf.add_page()

# fuente de la pagina del pdf 
pdf.set_font("Arial", size=12)

# Agregamos el texto que quetemos a la pagina
pdf.cell(200, 10, txt="Boleta restaurante", ln=True, align='C')

# Guardar el PDF
pdf.output("mi_primer_pdf.pdf")






