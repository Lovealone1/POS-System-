import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from detalle_compra import VistaDetallesCompra  # Asegúrate de reemplazar 'detalles_compra_view' con el nombre de tu archivo
from tkinter import messagebox
from pago_compra import VistaPago

class VistaCompras(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        # Date Picker
        self.fecha_label = tk.Label(self, text="Fecha:")
        self.fecha_label.grid(row=0, column=2, padx=(0, 215), pady=0, sticky='e')
        self.fecha_picker = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2,
                                      date_pattern='dd/mm/yyyy')
        self.fecha_picker.grid(row=0, column=2, padx=(0, 115), pady=0, sticky='e')

        # Botón de Filtrar por Fecha
        self.filtrar_fecha_button = tk.Button(self, text="Filtrar por Fecha", command=self.buscar_por_fecha)
        self.filtrar_fecha_button.grid(row=0, column=2, pady=10, padx=(0, 10), sticky='e')

        self.buscar_label = tk.Label(self, text="No de Compra:")
        self.buscar_label.grid(row=0, column=0, padx=(0, 450), pady=10, sticky='e')
        self.numero_compra_var = tk.StringVar()
        self.numero_compra_entry = tk.Entry(self, textvariable=self.numero_compra_var, width=12)
        self.numero_compra_entry.grid(row=0, column=0, padx=(0, 370), pady=10, sticky='e')

        # Modificar el nombre del método asociado al botón
        self.filtrar_compra_button = tk.Button(self, text="Buscar Compra", command=self.buscar_por_numero_compra)
        self.filtrar_compra_button.grid(row=0, column=0, pady=10, padx=(0, 270), sticky='e')

        self.lista_compras = ttk.Treeview(
            self, columns=('ID Compra', 'Fecha', 'Proveedor', 'Estado','Forma de pago', 'Total', 'Saldo Restante'),
            show='headings'
        )
        self.lista_compras.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky='nsew')

        self.lista_compras.column('ID Compra', width=100)
        self.lista_compras.column('Fecha', width=120)
        self.lista_compras.column('Proveedor', width=170)
        self.lista_compras.column('Total', width=100)
        self.lista_compras.column('Forma de pago', width=120)  # Cambiado el nombre de la columna
        self.lista_compras.column('Estado', width=100)
        self.lista_compras.column('Saldo Restante', width=150)  # Nueva columna


        self.lista_compras.heading('ID Compra', text='ID Compra')
        self.lista_compras.heading('Fecha', text='Fecha')
        self.lista_compras.heading('Proveedor', text='Proveedor')
        self.lista_compras.heading('Total', text='Total')
        self.lista_compras.heading('Forma de pago', text='Forma de pago')  # Cambiado el nombre del encabezado
        self.lista_compras.heading('Estado', text='Estado')
        self.lista_compras.heading('Saldo Restante', text='Saldo Restante')

        self.scrollbar_y = ttk.Scrollbar(self, orient='vertical', command=self.lista_compras.yview)
        self.scrollbar_y.grid(row=1, column=3, sticky='ns')
        self.lista_compras.configure(yscrollcommand=self.scrollbar_y.set)

        self.pago_facturas = tk.Button(self, text="Pago de facturas", command=self.abrir_pago_facturas)
        self.pago_facturas.grid(row=2, column=0, columnspan=3, padx=(35, 0), pady=10, sticky='w')
        self.rld = tk.Button(self, text="↻", command=self.actualizar_tabla)
        self.rld.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=10, sticky='w')

        self.ver_detalles_button = tk.Button(self, text="Ver Detalles", command=self.abrir_detalles)
        self.ver_detalles_button.grid(row=2, column=2, columnspan=3, padx=(184, 0), pady=10, sticky='w')
        self.eliminar_compra = tk.Button(self, text="Eliminar Compra", command=self.eliminar_compra)
        self.eliminar_compra.grid(row=2, column=2, columnspan=3, padx=(80, 0), pady=10, sticky='w')
        self.cargar_compras_desde_db()

    def actualizar_tabla(self):
        # Método para actualizar la tabla de compras
        self.lista_compras.delete(*self.lista_compras.get_children())
        self.cargar_compras_desde_db()
    def abrir_pago_facturas(self):
        # Método para manejar la acción del botón "Pago de facturas"
        selected_item = self.lista_compras.selection()
        if selected_item:
            # Obtener el ID de compra seleccionado
            id_compra = self.lista_compras.item(selected_item, 'values')[0]

            # Crear e instanciar VistaPagoCompra como una ventana emergente
            pago_compra_view = VistaPago(self.master, id_compra)

        else:
            messagebox.showinfo("Error", "Selecciona una compra para realizar el pago.")

    def actualizar_despues_pago(self, id_compra):
        # Método para realizar actualizaciones después del pago
        # Aquí puedes poner lógica para actualizar la vista o realizar otras acciones necesarias
        print(f"Pago realizado para la compra con ID: {id_compra}")

    def eliminar_compra(self):
        # Método para manejar la acción del botón "Eliminar Compra"
        selected_item = self.lista_compras.selection()
        if selected_item:
            # Obtener el ID de compra seleccionado
            id_compra = self.lista_compras.item(selected_item, 'values')[0]

            # Mostrar un messagebox de confirmación
            respuesta = messagebox.askquestion("Confirmar eliminación",
                                               "¿Estás seguro de que quieres eliminar esta compra")

            if respuesta == 'yes':
                try:
                    # Conectar a la base de datos
                    conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
                    cursor = conexion.cursor()

                    # Obtener forma_pago_id antes de eliminar la compra
                    cursor.execute("SELECT forma_pago_id, total, estado_compra FROM compras WHERE id = ?", (id_compra,))
                    resultado = cursor.fetchone()
                    forma_pago_id, total_compra, estado_compra = resultado[0], resultado[1], resultado[2]

                    # Obtener detalles de la compra para revertir la cantidad en productos
                    cursor.execute("SELECT id_producto, cantidad_producto FROM detalles_compra WHERE id_compra = ?",
                                   (id_compra,))
                    detalles_compra = cursor.fetchall()

                    # Eliminar los detalles de la compra de la tabla detalles_compra
                    cursor.execute("DELETE FROM detalles_compra WHERE id_compra = ?", (id_compra,))

                    # Eliminar la compra de la tabla compras
                    cursor.execute("DELETE FROM compras WHERE id = ?", (id_compra,))

                    # Actualizar el saldo en la tabla bancos
                    if forma_pago_id is not None:
                        cursor.execute("UPDATE bancos SET saldo = saldo + ? WHERE id = ?",
                                       (total_compra, forma_pago_id))

                    # Si el estado de la compra es 'Activa', actualizar la tabla compras_credito
                    if estado_compra == 'Activa':
                        cursor.execute("UPDATE compras_credito SET saldo = saldo - ? WHERE id = 1", (total_compra,))

                    # Revertir la cantidad en la tabla productos
                    for detalle in detalles_compra:
                        id_producto, cantidad_producto = detalle[0], detalle[1]
                        cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
                                       (cantidad_producto, id_producto))

                    # Confirmar y cerrar la conexión
                    conexion.commit()
                    conexion.close()

                    # Limpiar la lista de compras
                    self.lista_compras.delete(*self.lista_compras.get_children())

                    # Volver a cargar las compras desde la base de datos actualizada
                    self.cargar_compras_desde_db()

                except sqlite3.Error as e:
                    print(f"Error al eliminar compra desde la base de datos: {e}")

        else:
            messagebox.showinfo("Error", "Selecciona una compra para eliminar.")

    def abrir_detalles(self):
        # Método para manejar la acción del botón "Ver Detalles"
        selected_item = self.lista_compras.selection()
        if selected_item:
            # Obtener el ID de compra seleccionado
            id_compra = self.lista_compras.item(selected_item, 'values')[0]

            # Crear e instanciar VistaDetallesCompra como una ventana emergente
            detalles_compra_view = VistaDetallesCompra(self.master, id_compra)


        else:
            print("Selecciona una compra para ver detalles.")

    def filtrar_por_fecha(self):
        # Método para manejar la acción del botón "Filtrar por Fecha"
        selected_date = self.fecha_picker.get_date()
        # Implementar lógica para filtrar por la fecha seleccionada
        print(f"Filtrar por fecha: {selected_date}")

    def cargar_compras_desde_db(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener todas las compras
            cursor.execute(
                "SELECT id, fecha_compra, proveedor_id, estado_compra, forma_pago_id, total, saldo_restante FROM compras")

            # Obtener todas las compras
            compras = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Agregar las compras a la lista
            for compra in compras:
                proveedor_id = compra[2]
                proveedor_nombre = self.obtener_nombre_proveedor(proveedor_id)
                forma_pago_id = compra[4]
                nombre_banco = self.obtener_nombre_banco(forma_pago_id)  # Nuevo
                self.lista_compras.insert('', 'end', values=(
                    compra[0], compra[1], proveedor_nombre, compra[3], nombre_banco, compra[5], compra[6]
                ))

        except sqlite3.Error as e:
            print(f"Error al cargar compras desde la base de datos: {e}")

    def obtener_nombre_banco(self, forma_pago_id):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el nombre del banco
            cursor.execute("SELECT nombre_banco FROM bancos WHERE id = ?", (forma_pago_id,))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Verificar si se encontró el nombre del banco
            if resultado is not None:
                nombre_banco = resultado[0]
                return nombre_banco
            else:
                return "Credito"

        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del banco desde la base de datos: {e}")
            return "Error al obtener el nombre del banco"

    def obtener_nombre_proveedor(self, proveedor_id):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el nombre del proveedor
            cursor.execute("SELECT nombre FROM proveedores WHERE id_proveedor = ?", (proveedor_id,))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Verificar si se encontró el nombre del proveedor
            if resultado is not None:
                nombre_proveedor = resultado[0]
                return nombre_proveedor
            else:
                return "Proveedor no encontrado"

        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del proveedor desde la base de datos: {e}")
            return "Error al obtener el nombre del proveedor"

    def cerrar(self):
        # Método para cerrar la ventana del CRUD
        self.master.destroy()

    def conectar_base_datos(self, ruta_db):
        # Método para conectar a la base de datos
        try:
            self.conexion = sqlite3.connect(ruta_db)
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar_conexion(self):
        # Método para cerrar la conexión a la base de datos
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()

    def buscar_por_numero_compra(self):
        # Método para manejar la acción del botón "Buscar Compra"
        numero_compra = self.numero_compra_var.get()

        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para buscar por número de compra
            cursor.execute(
                "SELECT id, fecha_compra, proveedor_id, estado_compra, forma_pago_id, total FROM compras WHERE id = ?",
                (numero_compra,))

            # Obtener la compra encontrada
            compra_encontrada = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Limpiar la lista de compras
            self.lista_compras.delete(*self.lista_compras.get_children())
            self.numero_compra_var.set('')
            # Agregar la compra encontrada a la lista
            if compra_encontrada:
                proveedor_id = compra_encontrada[2]
                proveedor_nombre = self.obtener_nombre_proveedor(proveedor_id)
                self.lista_compras.insert('', 'end', values=(
                compra_encontrada[0], compra_encontrada[1], proveedor_nombre, compra_encontrada[3],
                compra_encontrada[4], compra_encontrada[5]))
            else:
                print(f"No se encontró ninguna compra con el número {numero_compra}")

        except sqlite3.Error as e:
            print(f"Error al buscar compra en la base de datos: {e}")

    def buscar_por_fecha(self):
        # Método para manejar la acción del botón "Buscar por Fecha"
        selected_date = self.fecha_picker.get_date()
        formatted_date = selected_date.strftime("%d/%m/%Y")

        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para buscar por fecha de compra
            cursor.execute(
                "SELECT id, fecha_compra, proveedor_id, estado_compra, forma_pago_id, total FROM compras WHERE fecha_compra = ?",
                (formatted_date,))

            # Obtener las compras encontradas
            compras_encontradas = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Limpiar la lista de compras
            self.lista_compras.delete(*self.lista_compras.get_children())

            # Agregar las compras encontradas a la lista
            for compra_encontrada in compras_encontradas:
                proveedor_id = compra_encontrada[2]
                proveedor_nombre = self.obtener_nombre_proveedor(proveedor_id)
                self.lista_compras.insert('', 'end', values=(
                    compra_encontrada[0], compra_encontrada[1], proveedor_nombre, compra_encontrada[3],
                    compra_encontrada[4], compra_encontrada[5]))

        except sqlite3.Error as e:
            print(f"Error al buscar compras por fecha en la base de datos: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaCompras(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
    app.grid()
    root.geometry("1200x600")
    root.mainloop()
