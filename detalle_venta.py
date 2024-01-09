import tkinter as tk
from tkinter import ttk
import sqlite3

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime


class VistaDetallesVenta(tk.Toplevel):
    def __init__(self, master=None, id_venta=None):
        super().__init__(master)
        self.master = master

        self.id_venta = id_venta

        self.tree = ttk.Treeview(self, columns=('ID Producto', 'Nombre Producto', 'Cantidad', 'Precio', 'Total'), show='headings')
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.tree.column('ID Producto', width=80)
        self.tree.column('Nombre Producto', width=150)
        self.tree.column('Cantidad', width=80)
        self.tree.column('Precio', width=80)
        self.tree.column('Total', width=80)

        self.tree.heading('ID Producto', text='ID Producto')
        self.tree.heading('Nombre Producto', text='Nombre Producto')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Total', text='SubTotal')

        self.scrollbar_y = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.cargar_detalles_compra_desde_db()

        self.btn_generar_factura = tk.Button(self, text="Generar Factura", command=self.generar_factura)
        self.btn_generar_factura.grid(row=1, column=0, pady=3, sticky='e', padx=(0, 10))
        self.obtener_info_cliente(self.obtener_cliente_id())
    def cargar_detalles_compra_desde_db(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener los detalles de la compra
            cursor.execute("SELECT id_producto, cantidad_producto, precio_producto FROM detalles_venta WHERE id_venta = ?", (self.id_venta,))

            # Obtener los detalles de la compra
            detalles_compra = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Agregar los detalles de la compra a la lista
            for detalle in detalles_compra:
                id_producto = detalle[0]
                nombre_producto = self.obtener_nombre_producto(id_producto)
                cantidad = detalle[1]
                precio = detalle[2]
                total = cantidad * precio
                self.tree.insert('', 'end', values=(id_producto, nombre_producto, cantidad, precio, total))

        except sqlite3.Error as e:
            print(f"Error al cargar detalles de la compra desde la base de datos: {e}")



    def obtener_nombre_producto(self, id_producto):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el nombre del producto
            cursor.execute("SELECT referencia FROM productos WHERE id = ?", (id_producto,))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Verificar si se encontró el nombre del producto
            if resultado is not None:
                nombre_producto = resultado[0]
                return nombre_producto
            else:
                return "Producto no encontrado"

        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del producto desde la base de datos: {e}")
            return "Error al obtener el nombre del producto"

    def generar_factura(self):
        try:
            # Obtener información del cliente
            cliente_info = self.obtener_info_cliente(self.obtener_cliente_id())

            # Nombre del archivo PDF
            nombre_archivo = f"factura_venta_{self.id_venta}.pdf"

            # Crear un lienzo PDF con ancho total
            pdf = SimpleDocTemplate(nombre_archivo, pagesize=letter)

            # Crear un objeto de estilo de texto
            estilo_texto = getSampleStyleSheet()["Normal"]

            # Crear un objeto de estilo para el total de la factura
            estilo_total = ParagraphStyle(
                "TotalFactura",
                parent=estilo_texto,
                fontSize=11,
                textColor=colors.black,
                spaceAfter=4,  # Ajusta según tu preferencia
                alignment=0,  # Alineado a la izquierda
                leftIndent=300,  # Ajusta según tu preferencia
            )

            # Crear un objeto de texto para el encabezado
            encabezado_texto = "Alveiro Garcia Loaiza\nNIT: 100000000-5\nCarrera 35 #3746\nCel: 3225711760 Medellin - Antioquia"

            # Separar el texto en líneas
            lineas_encabezado = encabezado_texto.split('\n')

            estilo_encabezado = ParagraphStyle(
                "Encabezado",
                parent=estilo_texto,
                fontName='Helvetica-Bold',
                fontSize=14,
            )

            # Crear un objeto de texto para cada línea del encabezado
            texto_encabezado = []

            # Agregar un espacio adicional después de "Alveiro Garcia Loaiza"
            texto_encabezado.append(Paragraph(lineas_encabezado[0], estilo_encabezado))
            texto_encabezado.append(Spacer(1, 12))

            for i, linea in enumerate(lineas_encabezado[1:]):
                texto_encabezado.append(Paragraph(linea, estilo_texto))

            # Obtener la fecha actual y formatearla
            fecha_expedicion = datetime.now().strftime("%d/%m/%Y")

            # Agregar la fecha de expedición en medio del encabezado y los datos del cliente
            texto_encabezado.append(Spacer(1, 12))
            texto_encabezado.append(Paragraph(f"Fecha de Expedición: {fecha_expedicion}", estilo_texto))
            texto_encabezado.append(Spacer(1, 12))

            # Agregar el texto del cliente a la factura
            texto_encabezado.append(Paragraph(f"Cliente: {cliente_info[1]} - CC/NIT: {cliente_info[0]}", estilo_texto))
            texto_encabezado.append(
                Paragraph(f"Dirección: {cliente_info[2]} - Celular: {cliente_info[3]}", estilo_texto))
            texto_encabezado.append(Paragraph(f"Correo: {cliente_info[4]}", estilo_texto))
            texto_encabezado.append(Paragraph(f"Ciudad: {cliente_info[5]}", estilo_texto))
            texto_encabezado.append(Spacer(1, 22))

            # Lista para almacenar los datos de la tabla
            data = [['ID Producto', 'Nombre Producto', 'Cantidad', 'Valor Unitario', 'Valor total']]

            # Agregar detalles de la compra a la lista
            for item in self.tree.get_children():
                values = self.tree.item(item, 'values')
                id_producto, nombre_producto, cantidad, precio, total = values
                subtotal = float(cantidad) * float(precio)
                data.append(
                    [id_producto, nombre_producto, float(cantidad), f"${float(precio):.2f}", f"${float(subtotal):.2f}"])

            # Definir el ancho de cada columna
            col_widths = [50, 150, 50, 80, 80]

            # Calcular el alto de cada fila (usando el mismo alto para todas las filas)
            row_height = 20

            # Crear la tabla
            tabla = Table(data, colWidths=col_widths, rowHeights=row_height)

            # Establecer el estilo de la tabla
            estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                       ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                       ])

            tabla.setStyle(estilo_tabla)

            # Agregar el texto y la tabla al lienzo PDF
            contenido_pdf = texto_encabezado + [tabla]

            # Calcular el total de la factura
            total_factura = sum(float(self.tree.item(item, 'values')[-1]) for item in self.tree.get_children())
            contenido_pdf.append(Spacer(1, 400))
            # Agregar el total de la factura al contenido del PDF
            contenido_pdf.append(Spacer(1, 12))
            contenido_pdf.append(Paragraph(f"Total a pagar: ${total_factura:.2f}", estilo_total))

            # Construir el PDF con el contenido modificado
            pdf.build(contenido_pdf)

            print(f"Factura generada: {nombre_archivo}")

        except Exception as e:
            print(f"Error al generar la factura: {e}")

    def obtener_cliente_id(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el cliente_id de la tabla ventas
            cursor.execute("SELECT cliente_id FROM ventas WHERE id = ?", (self.id_venta,))
            cliente_id = cursor.fetchone()[0]

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()
            return cliente_id

        except sqlite3.Error as e:
            print(f"Error al obtener el cliente_id desde la base de datos: {e}")
            return None

    def obtener_info_cliente(self, cliente_id):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener la información del cliente
            cursor.execute(
                "SELECT cc_nit, nombre, direccion, celular, correo, ciudad FROM clientes WHERE id_cliente = ?",
                (cliente_id,))
            info_cliente = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            return info_cliente

        except sqlite3.Error as e:
            print(f"Error al obtener la información del cliente desde la base de datos: {e}")
            return None


if __name__ == "__main__":
    # Supongamos que tienes el ID de la compra que deseas ver los detalles

    root = tk.Tk()
    root.mainloop()
