import tkinter as tk
from tkinter import ttk
import sqlite3

class VistaDetallesCompra(tk.Toplevel):
    def __init__(self, master=None, id_compra=None):
        super().__init__(master)
        self.master = master

        self.id_compra = id_compra

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

    def cargar_detalles_compra_desde_db(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener los detalles de la compra
            cursor.execute("SELECT id_producto, cantidad_producto, precio_producto FROM detalles_compra WHERE id_compra = ?", (self.id_compra,))

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



if __name__ == "__main__":
    # Supongamos que tienes el ID de la compra que deseas ver los detalles

    root = tk.Tk()
    root.mainloop()
