import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from detalle_venta import VistaDetallesVenta  # Asegúrate de reemplazar 'detalles_compra_view' con el nombre de tu archivo
from tkinter import messagebox
from pago_venta import VistaPagoVenta

class VistaVentas(tk.Frame):
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

        self.buscar_label = tk.Label(self, text="No de venta:")
        self.buscar_label.grid(row=0, column=0, padx=(0, 525), pady=10, sticky='e')
        self.numero_venta_var = tk.StringVar()
        self.numero_venta_entry = tk.Entry(self, textvariable=self.numero_venta_var, width=8)
        self.numero_venta_entry.grid(row=0, column=0, padx=(0, 470), pady=10, sticky='e')

        # Modificar el nombre del método asociado al botón
        self.filtrar_venta_button = tk.Button(self, text="Buscar venta", command=self.buscar_por_numero_venta)
        self.filtrar_venta_button.grid(row=0, column=0, pady=10, padx=(0, 383), sticky='e')

        clientes=[]
        self.buscar_cliente_label = tk.Label(self, text="Cliente:")
        self.buscar_cliente_label.grid(row=0, column=0, padx=(0, 280), pady=10, sticky='e')
        self.nombre_cliente_var = tk.StringVar()
        self.nombre_cliente_combobox = ttk.Combobox(self, textvariable=self.nombre_cliente_var, width=18)
        self.nombre_cliente_combobox.grid(row=0, column=0, padx=(0, 150), pady=10, sticky='e')

        # Modificar el nombre del método asociado al botón
        self.filtrar_cliente_button = tk.Button(self, text="Buscar venta", command=self.buscar_por_cliente)
        self.filtrar_cliente_button.grid(row=0, column=0, pady=10, padx=(0, 64), sticky='e')

        self.lista_ventas = ttk.Treeview(
            self, columns=('ID Venta', 'Fecha', 'Cliente', 'Estado','Forma de pago', 'Total', 'Saldo Restante'),
            show='headings'
        )
        self.lista_ventas.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky='nsew')

        self.lista_ventas.column('ID Venta', width=100)
        self.lista_ventas.column('Fecha', width=120)
        self.lista_ventas.column('Cliente', width=170)
        self.lista_ventas.column('Total', width=100)
        self.lista_ventas.column('Forma de pago', width=120)  # Cambiado el nombre de la columna
        self.lista_ventas.column('Estado', width=100)
        self.lista_ventas.column('Saldo Restante', width=150)  # Nueva columna


        self.lista_ventas.heading('ID Venta', text='ID Venta')
        self.lista_ventas.heading('Fecha', text='Fecha')
        self.lista_ventas.heading('Cliente', text='Cliente')
        self.lista_ventas.heading('Total', text='Total')
        self.lista_ventas.heading('Forma de pago', text='Forma de pago')  # Cambiado el nombre del encabezado
        self.lista_ventas.heading('Estado', text='Estado')
        self.lista_ventas.heading('Saldo Restante', text='Saldo Restante')

        self.scrollbar_y = ttk.Scrollbar(self, orient='vertical', command=self.lista_ventas.yview)
        self.scrollbar_y.grid(row=1, column=3, sticky='ns')
        self.lista_ventas.configure(yscrollcommand=self.scrollbar_y.set)

        self.pago_facturas = tk.Button(self, text="Pago de facturas", command=self.abrir_pago_facturas)
        self.pago_facturas.grid(row=2, column=0, columnspan=3, padx=(35, 0), pady=10, sticky='w')
        self.rld = tk.Button(self, text="↻", command=self.actualizar_tabla)
        self.rld.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=10, sticky='w')

        self.ver_detalles_button = tk.Button(self, text="Ver Detalles", command=self.abrir_detalles)
        self.ver_detalles_button.grid(row=2, column=2, columnspan=3, padx=(184, 0), pady=10, sticky='w')
        self.eliminar_compra = tk.Button(self, text="Eliminar Venta", command=self.eliminar_compra)
        self.eliminar_compra.grid(row=2, column=2, columnspan=3, padx=(80, 0), pady=10, sticky='w')
        self.cargar_compras_desde_db()
        self.cargar_clientes_desde_db()

    def cargar_clientes_desde_db(self):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener los proveedores
            cursor.execute("SELECT nombre FROM clientes")

            # Obtener todos los proveedores
            clientes = [nombre[0] for nombre in cursor.fetchall()]

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar los proveedores en el Combobox
            self.nombre_cliente_combobox['values'] = clientes

        except sqlite3.Error as e:
            print(f"Error al cargar proveedores desde la base de datos: {e}")

    def obtener_id_cliente_desde_venta(self):
        try:
            # Obtener el nombre del cliente seleccionado en el Combobox
            nombre_cliente_seleccionado = self.nombre_cliente_combobox.get()

            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL SELECT para obtener el cliente_id asociado a la venta
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (nombre_cliente_seleccionado,))

            # Obtener el resultado de la consulta
            result = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Verificar si hay resultados antes de intentar acceder al elemento
            if result is not None:
                cliente_id = result[0]
                return cliente_id
            else:
                print("No se encontró cliente asociado a la venta.")
                return None

        except sqlite3.Error as e:
            print(f"Error al obtener el ID del cliente desde la venta en la base de datos: {e}")
            return None

    def buscar_por_cliente(self):
        try:
            # Obtener el id del cliente seleccionado en el Combobox
            id_cliente = self.obtener_id_cliente_desde_venta()

            if id_cliente is not None:
                # Conectar a la base de datos
                self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
                cursor = self.conexion.cursor()

                # Ejecutar la consulta SQL para buscar por id_cliente
                cursor.execute(
                    "SELECT id, fecha_venta, cliente_id, estado_venta, forma_pago_id, total,saldo_restante FROM ventas WHERE cliente_id = ?",
                    (id_cliente,))

                # Obtener las ventas encontradas
                ventas_encontradas = cursor.fetchall()

                # Cerrar el cursor y la conexión
                cursor.close()
                self.cerrar_conexion()

                # Limpiar la lista de ventas
                self.lista_ventas.delete(*self.lista_ventas.get_children())

                # Agregar las ventas encontradas a la lista
                for venta_encontrada in ventas_encontradas:
                    cliente_id = venta_encontrada[2]
                    cliente_nombre = self.obtener_nombre_cliente(cliente_id)
                    self.lista_ventas.insert('', 'end', values=(
                        venta_encontrada[0], venta_encontrada[1], cliente_nombre, venta_encontrada[3],
                        venta_encontrada[4], venta_encontrada[5],venta_encontrada[6]))

            else:
                print("No se pudo obtener el ID del cliente para la búsqueda.")

        except sqlite3.Error as e:
            print(f"Error al buscar ventas por cliente en la base de datos: {e}")

    def actualizar_tabla(self):
        # Método para actualizar la tabla de compras
        self.lista_ventas.delete(*self.lista_ventas.get_children())
        self.cargar_compras_desde_db()

    def abrir_pago_facturas(self):
        # Método para manejar la acción del botón "Pago de facturas"
        selected_item = self.lista_ventas.selection()
        if selected_item:
            # Obtener el ID de compra seleccionado
            id_compra = self.lista_ventas.item(selected_item, 'values')[0]

            # Crear e instanciar VistaPagoCompra como una ventana emergente
            pago_compra_view = VistaPagoVenta(self.master, id_compra)

        else:
            messagebox.showinfo("Error", "Selecciona una compra para realizar el pago.")

    def actualizar_despues_pago(self, id_compra):
        # Método para realizar actualizaciones después del pago
        # Aquí puedes poner lógica para actualizar la vista o realizar otras acciones necesarias
        print(f"Pago realizado para la compra con ID: {id_compra}")

    def eliminar_compra(self):
        # Método para manejar la acción del botón "Eliminar Compra"
        selected_item = self.lista_ventas.selection()
        if selected_item:
            # Obtener el ID de compra seleccionado
            id_venta = self.lista_ventas.item(selected_item, 'values')[0]

            # Mostrar un messagebox de confirmación
            respuesta = messagebox.askquestion("Confirmar eliminación",
                                               "¿Estás seguro de que quieres eliminar esta venta")

            if respuesta == 'yes':
                try:
                    # Conectar a la base de datos
                    conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
                    cursor = conexion.cursor()

                    # Obtener forma_pago_id antes de eliminar la compra
                    cursor.execute("SELECT forma_pago_id, total, estado_venta FROM ventas WHERE id = ?", (id_venta,))
                    resultado = cursor.fetchone()
                    forma_pago_id, total_venta, estado_venta = resultado[0], resultado[1], resultado[2]

                    # Obtener detalles de la compra para revertir la cantidad en productos
                    cursor.execute("SELECT id_producto, cantidad_producto FROM detalles_venta WHERE id_venta = ?",
                                   (id_venta,))
                    detalles_venta = cursor.fetchall()

                    cursor.execute("SELECT cliente_id FROM ventas WHERE id = ?", (id_venta,))
                    cliente_id = cursor.fetchone()[0]
                    print(cliente_id)

                    # Eliminar los detalles de la compra de la tabla detalles_compra
                    cursor.execute("DELETE FROM detalles_venta WHERE id_venta = ?", (id_venta,))

                    # Eliminar la compra de la tabla compras
                    cursor.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))

                    # Actualizar el saldo en la tabla bancos
                    if forma_pago_id is not None:
                        cursor.execute("UPDATE bancos SET saldo = saldo - ? WHERE id = ?",
                                       (total_venta, forma_pago_id))

                    # Si el estado de la compra es 'Activa', actualizar la tabla compras_credito
                    if estado_venta == 'Activa':
                        # Obtener el cliente_id asociado a la venta

                        # Actualizar el saldo en la tabla de clientes
                        cursor.execute("UPDATE clientes SET saldo = saldo - ? WHERE id_cliente = ?",
                                       (total_venta, cliente_id))

                        cursor.execute("UPDATE ventas_credito SET saldo = saldo - ? WHERE id = 1", (total_venta,))

                    # Revertir la cantidad en la tabla productos
                    for detalle in detalles_venta:
                        id_producto, cantidad_producto = detalle[0], detalle[1]
                        cursor.execute("UPDATE productos SET cantidad = cantidad + ? WHERE id = ?",
                                       (cantidad_producto, id_producto))

                    # Confirmar y cerrar la conexión
                    conexion.commit()
                    conexion.close()

                    # Limpiar la lista de compras
                    self.lista_ventas.delete(*self.lista_ventas.get_children())

                    # Volver a cargar las compras desde la base de datos actualizada
                    self.cargar_compras_desde_db()

                except sqlite3.Error as e:
                    print(f"Error al eliminar compra desde la base de datos: {e}")

        else:
            messagebox.showinfo("Error", "Selecciona una compra para eliminar.")

    def abrir_detalles(self):
        # Método para manejar la acción del botón "Ver Detalles"
        selected_item = self.lista_ventas.selection()
        if selected_item:
            # Obtener el ID de compra seleccionado
            id_compra = self.lista_ventas.item(selected_item, 'values')[0]

            # Crear e instanciar VistaDetallesCompra como una ventana emergente
            detalles_venta_view = VistaDetallesVenta(self.master, id_compra)


        else:
            print("Selecciona una compra para ver detalles.")

    def filtrar_por_fecha(self):
        # Método para manejar la acción del botón "Filtrar por Fecha"
        selected_date = self.fecha_picker.get_date()
        # Implementar lógica para filtrar por la fecha seleccionada
        print(f"Filtrar por fecha: {selected_date}")

    def buscar_por_numero_venta(self):
        # Método para manejar la acción del botón "Buscar Compra"
        numero_venta = self.numero_venta_var.get()

        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para buscar por número de compra
            cursor.execute(
                "SELECT id, fecha_venta, cliente_id, estado_venta, forma_pago_id, total FROM ventas WHERE id = ?",
                (numero_venta,))

            # Obtener la compra encontrada
            venta_encontrada = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Limpiar la lista de compras
            self.lista_ventas.delete(*self.lista_ventas.get_children())
            self.numero_venta_var.set('')
            # Agregar la compra encontrada a la lista
            if venta_encontrada:
                cliente_id = venta_encontrada[2]
                proveedor_nombre = self.obtener_nombre_cliente(cliente_id)
                self.lista_ventas.insert('', 'end', values=(
                venta_encontrada[0], venta_encontrada[1], proveedor_nombre, venta_encontrada[3],
                venta_encontrada[4], venta_encontrada[5]))
            else:
                print(f"No se encontró ninguna compra con el número {numero_venta}")

        except sqlite3.Error as e:
            print(f"Error al buscar compra en la base de datos: {e}")

    def cargar_compras_desde_db(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener todas las compras
            cursor.execute(
                "SELECT id, fecha_venta, cliente_id, estado_venta, forma_pago_id, total, saldo_restante FROM ventas")

            # Obtener todas las compras
            compras = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Agregar las compras a la lista
            for compra in compras:
                cliente_id = compra[2]
                proveedor_nombre = self.obtener_nombre_cliente(cliente_id)
                forma_pago_id = compra[4]
                nombre_banco = self.obtener_nombre_banco(forma_pago_id)  # Nuevo
                self.lista_ventas.insert('', 'end', values=(
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

    def obtener_nombre_cliente(self, cliente_id):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el nombre del proveedor
            cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = ?", (cliente_id,))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Verificar si se encontró el nombre del proveedor
            if resultado is not None:
                nombre_cliente = resultado[0]
                return nombre_cliente
            else:
                return "Cliente no encontrado"

        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del cliente desde la base de datos: {e}")
            return "Error al obtener el nombre del cliente"

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
                "SELECT id, fecha_venta, cliente_id, estado_venta, forma_pago_id, total FROM ventas WHERE fecha_venta = ?",
                (formatted_date,))

            # Obtener las compras encontradas
            ventas_encontradas = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Limpiar la lista de compras
            self.lista_ventas.delete(*self.lista_ventas.get_children())

            # Agregar las compras encontradas a la lista
            for venta_encontrada in ventas_encontradas:
                proveedor_id = venta_encontrada[2]
                proveedor_nombre = self.obtener_nombre_cliente(proveedor_id)
                self.lista_ventas.insert('', 'end', values=(
                    venta_encontrada[0], venta_encontrada[1], proveedor_nombre, venta_encontrada[3],
                    venta_encontrada[4], venta_encontrada[5]))

        except sqlite3.Error as e:
            print(f"Error al buscar compras por fecha en la base de datos: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaVentas(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
    app.grid()
    root.mainloop()
