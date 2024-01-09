import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry


class VistaUtilidades(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Crear variables para almacenar las fechas seleccionadas
        self.fecha_inicio = tk.StringVar()
        self.fecha_fin = tk.StringVar()

        # Crear un contenedor Frame para los widgets relacionados
        frame_fechas = tk.Frame(self)
        frame_fechas.pack(pady=5, padx=5, anchor=tk.W)

        # Crear los DateEntry para seleccionar fechas
        self.datepicker_inicio = DateEntry(frame_fechas, width=12, background='darkblue', foreground='white',
                                           borderwidth=2, textvariable=self.fecha_inicio, date_pattern='dd/mm/yyyy')
        self.datepicker_fin = DateEntry(frame_fechas, width=12, background='darkblue', foreground='white',
                                        borderwidth=2, textvariable=self.fecha_fin, date_pattern='dd/mm/yyyy')

        # Configurar etiquetas para las fechas
        tk.Label(frame_fechas, text="Fecha Inicio:").pack(side=tk.LEFT, padx=(0, 5))
        self.datepicker_inicio.pack(side=tk.LEFT)
        tk.Label(frame_fechas, text="Fecha Fin:").pack(side=tk.LEFT, padx=(10, 5))
        self.datepicker_fin.pack(side=tk.LEFT)

        # Crear el botón Filtrar
        tk.Button(frame_fechas, text="Buscar por fecha", command=self.filtrar_utilidades).pack(side=tk.LEFT, pady=5, padx=5)

        # Crear la tabla para detalles de la compra
        self.crear_tabla_detalles_compra()

        # Crear el Label para mostrar la suma de utilidades
        self.label_suma_utilidades = tk.Label(self, text="Suma Utilidades: $0.00", font=("Arial", 11, "normal"))
        self.label_suma_utilidades.pack(side=tk.BOTTOM, padx=0, pady=10, anchor=tk.E)

        # Llamamos al método para cargar todas las utilidades
        self.cargar_todas_utilidades_desde_db()

    def crear_tabla_detalles_compra(self):
        # Código para crear la tabla de detalles de la compra
        self.tree_detalles_compra = ttk.Treeview(
            self, columns=('ID Venta', 'Nombre Producto', 'Cantidad', 'Precio Compra', 'Precio Venta', 'Utilidad', 'Fecha Venta'),
            show='headings'
        )
        self.tree_detalles_compra.pack(pady=0)

        # Definir encabezados de columna
        self.tree_detalles_compra.column('ID Venta', width=100)
        self.tree_detalles_compra.column('Nombre Producto', width=150)
        self.tree_detalles_compra.column('Cantidad', width=100)
        self.tree_detalles_compra.column('Precio Compra', width=120)
        self.tree_detalles_compra.column('Precio Venta', width=120)
        self.tree_detalles_compra.column('Utilidad', width=120)
        self.tree_detalles_compra.column('Fecha Venta', width=120)

        self.tree_detalles_compra.heading('ID Venta', text='ID Venta')
        self.tree_detalles_compra.heading('Nombre Producto', text='Nombre Producto')
        self.tree_detalles_compra.heading('Cantidad', text='Cantidad')
        self.tree_detalles_compra.heading('Precio Compra', text='Precio Compra')
        self.tree_detalles_compra.heading('Precio Venta', text='Precio Venta')
        self.tree_detalles_compra.heading('Utilidad', text='Utilidad')
        self.tree_detalles_compra.heading('Fecha Venta', text='Fecha Venta')

        # Agregar barra de desplazamiento vertical
        scrollbar_y_detalles_compra = ttk.Scrollbar(self, orient='vertical', command=self.tree_detalles_compra.yview)
        scrollbar_y_detalles_compra.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_detalles_compra.configure(yscrollcommand=scrollbar_y_detalles_compra.set)


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

    def cargar_todas_utilidades_desde_db(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener todas las utilidades con información de productos
            cursor.execute(
                "SELECT u.id_venta, u.id_producto, u.cantidad_producto, u.precio_compra, u.precio_producto, u.utilidad, u.fecha_venta, p.referencia "
                "FROM utilidades u "
                "INNER JOIN productos p ON u.id_producto = p.id"
            )

            # Obtener todas las utilidades con información de productos
            utilidades = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Limpiar la lista de detalles de la compra
            self.tree_detalles_compra.delete(*self.tree_detalles_compra.get_children())

            # Agregar todas las utilidades a la tabla
            suma_utilidades = 0
            for utilidad in utilidades:
                id_venta, id_producto, cantidad, precio_compra, precio_venta, utilidad, fecha_venta, nombre_producto = utilidad
                self.tree_detalles_compra.insert('', 'end', values=(
                    id_venta, nombre_producto, cantidad, precio_compra, precio_venta, utilidad, fecha_venta))
                suma_utilidades += utilidad

            # Actualizar el texto del Label con la suma de utilidades en formato de pesos
            self.label_suma_utilidades.config(text=f"Suma Utilidades: ${suma_utilidades:.2f}")

        except sqlite3.Error as e:
            print(f"Error al cargar todas las utilidades desde la base de datos: {e}")

    def filtrar_utilidades(self):
        # Obtener las fechas seleccionadas
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()

        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para filtrar utilidades por fechas
            cursor.execute(
                "SELECT id_venta, id_producto, cantidad_producto, precio_compra, precio_producto, utilidad, fecha_venta FROM utilidades "
                "WHERE fecha_venta BETWEEN ? AND ?",
                (fecha_inicio, fecha_fin)
            )

            # Obtener utilidades filtradas
            utilidades_filtradas = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Limpiar la lista de detalles de la compra
            self.tree_detalles_compra.delete(*self.tree_detalles_compra.get_children())

            # Agregar utilidades filtradas a la tabla
            suma_utilidades = 0
            for utilidad in utilidades_filtradas:
                id_venta, nombre_producto, cantidad, precio_compra, precio_venta, utilidad, fecha_venta = utilidad

                self.tree_detalles_compra.insert('', 'end', values=(
                    id_venta, nombre_producto, cantidad, precio_compra, precio_venta, utilidad, fecha_venta))
                suma_utilidades += utilidad

            # Actualizar el texto del Label con la suma de utilidades en formato de pesos
            self.label_suma_utilidades.config(text=f"Suma Utilidades: ${suma_utilidades:.2f}")

        except sqlite3.Error as e:
            print(f"Error al filtrar utilidades desde la base de datos: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    utilidades_view = VistaUtilidades(root)
    root.mainloop()
