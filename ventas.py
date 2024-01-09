import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from tkinter import messagebox
class VentaCRUD(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ventana de Ventas")
        # Variables de control
        self.numero_venta_var = tk.StringVar()
        self.cliente_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.metodo_pago_var = tk.StringVar()
        self.precio_var = tk.DoubleVar()
        self.cantidad_var = tk.DoubleVar()
        self.numero_venta_actual = tk.StringVar()
        self.label_cliente = tk.Label(self, text="Cliente:")
        self.label_cliente.grid(row=1, column=0, sticky="e")
        self.descripcion_var = tk.StringVar()

        self.ultima_venta_visual = tk.StringVar()
        self.obtener_ultima_venta_visual()

        # Simulamos una lista de proveedores para el ejemplo
        clientes = []
        self.proveedor_dropdown = ttk.Combobox(self, textvariable=self.cliente_var, values=clientes)
        self.proveedor_dropdown.grid(row=1, column=1)

        self.label_descripcion = tk.Label(self, text="Descripción:")
        self.label_descripcion.grid(row=1, column=0, sticky="e")
        self.entry_descripcion = tk.Entry(self, textvariable=self.descripcion_var, width=10)
        self.entry_descripcion.grid(row=1, column=1, padx=(0, 82))
        self.btn_buscar_descripcion = tk.Button(self, text="Filtrar", command=self.buscar_descripcion)
        self.btn_buscar_descripcion.grid(row=1, column=1, padx=(30, 0))

        self.label_producto = tk.Label(self, text="Producto:")
        self.label_producto.grid(row=2, column=0, sticky="e")
        # Cargar productos desde la base de datos
        self.cargar_productos_desde_db()
        self.label_fecha_venta = tk.Label(self, text="Fecha de venta:")
        self.label_fecha_venta.grid(row=2, column=0, sticky="e")

        # Utilizar el widget DateEntry para seleccionar la fecha
        self.fecha_venta_var = tk.StringVar()
        self.fecha_venta_entry = DateEntry(self, textvariable=self.fecha_venta_var, date_pattern='dd/MM/yyyy')
        self.fecha_venta_entry.grid(row=2, column=1)

        # Usar un Combobox para seleccionar el producto
        self.producto_dropdown = ttk.Combobox(self, textvariable=self.producto_var, values=self.productos)
        self.producto_dropdown.grid(row=2, column=1)

        self.entry_numero_venta = tk.Entry(self, textvariable=self.ultima_venta_visual, state="readonly")
        self.entry_numero_venta.grid(row=0, column=1, padx=(10, 0))

        self.label_stock = tk.Label(self, text="Stock:")
        self.label_stock.grid(row=6, column=0, sticky="e")
        self.stock_producto_var = tk.StringVar()
        self.entry_stock = tk.Entry(self, textvariable=self.stock_producto_var, state="readonly")
        self.entry_stock.grid(row=6, column=1)

        # Etiqueta y campo de entrada para el precio
        self.label_precio = tk.Label(self, text="Precio:")
        self.label_precio.grid(row=4, column=0, sticky="e")
        self.entry_precio = tk.Entry(self, textvariable=self.precio_var)
        self.entry_precio.grid(row=4, column=1)

        self.label_cantidad = tk.Label(self, text="Cantidad:")
        self.label_cantidad.grid(row=5, column=0, sticky="e")
        self.entry_cantidad = tk.Entry(self, textvariable=self.cantidad_var)
        self.entry_cantidad.grid(row=5, column=1)

        self.producto_dropdown.grid_remove()
        self.label_producto.grid_remove()
        self.label_precio.grid_remove()
        self.entry_precio.grid_remove()
        self.label_cantidad.grid_remove()
        self.entry_cantidad.grid_remove()
        self.label_stock.grid_remove()
        self.entry_stock.grid_remove()
        self.entry_descripcion.grid_remove()
        self.label_descripcion.grid_remove()
        self.btn_buscar_descripcion.grid_remove()

        # Utilizar el Combobox actualizado con las cuentas
        self.label_cuenta = tk.Label(self, text="Cuenta:")
        self.label_cuenta.grid(row=9, column=4, padx=(90, 0))
        self.cuenta_var = tk.StringVar()
        cuentas = []
        self.cuenta_dropdown = ttk.Combobox(self, textvariable=self.cuenta_var, values=cuentas)
        self.cuenta_dropdown.grid(row=9, column=4, padx=(290, 0))

        self.btn_insertar_venta = tk.Button(self, text="Generar venta", command=self.insertar_venta)
        self.btn_insertar_venta.grid(row=0, column=0, columnspan=2, pady=10, padx=(0, 140))

        self.btn_agregar = tk.Button(self, text="Agregar producto", command=self.agregar)
        self.btn_agregar.grid(row=9, column=0, columnspan=2, padx=(90, 0), pady=10)

        self.btn_finalizar_venta = tk.Button(self, text="Finalizar Compra", command=self.finalizar_compra_independiente)
        self.btn_finalizar_venta.grid(row=9, column=5, pady=5, columnspan=1, padx=(0, 30), sticky='e')

        self.btn_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar)
        self.btn_eliminar.grid(row=9, column=0, columnspan=2, pady=10,padx=(0,80))

        self.lista = ttk.Treeview(self, columns=('ID Producto', 'Cantidad', 'Precio', 'ID Venta', 'Subtotal'),
                                  show='headings')
        self.lista.grid(row=0, rowspan=8, column=2, columnspan=4, pady=10, padx=(20,20))
        self.lista.heading('ID Producto', text='ID Producto')
        self.lista.heading('Cantidad', text='Cantidad')
        self.lista.heading('Precio', text='Precio')
        self.lista.heading('ID Venta', text='ID Venta')
        self.lista.heading('Subtotal', text='Subtotal')
        self.lista.column('ID Producto', width=100, anchor=tk.CENTER)
        self.lista.column('Cantidad', width=100, anchor=tk.CENTER)
        self.lista.column('Precio', width=100, anchor=tk.CENTER)
        self.lista.column('ID Venta', width=100, anchor=tk.CENTER)
        self.lista.column('Subtotal', width=100, anchor=tk.CENTER)
        self.label_modo_pago = tk.Label(self, text="Modo de Pago:")
        self.label_modo_pago.grid(row=9, column=5,padx=(0,286))
        modos_pago = ["Crédito", "Contado"]
        self.modo_pago_dropdown = ttk.Combobox(self, textvariable=self.metodo_pago_var, values=modos_pago)
        self.modo_pago_dropdown.grid(row=9, column=5,padx=(0, 50))

        self.label_cuenta.grid_remove()
        self.cuenta_dropdown.grid_remove()
        self.btn_agregar.grid_remove()
        self.btn_eliminar.grid_remove()
        self.label_modo_pago.grid_remove()
        self.modo_pago_dropdown.grid_remove()
        self.btn_finalizar_venta.grid_remove()
        self.label_cuenta.grid_remove()
        self.cuenta_dropdown.grid_remove()


        # Evento de selección de la lista
        self.lista.bind('<ButtonRelease-1>', self.cargar_registro_seleccionado)
        self.cuenta_dropdown.bind("<<ComboboxSelected>>", self.obtener_id_banco_desde_combobox)
        self.modo_pago_dropdown.bind("<<ComboboxSelected>>", self.actualizar_dropdown_cuentas)
        self.producto_dropdown.bind("<<ComboboxSelected>>", self.actualizar_info_en_entries)
        self.cliente_var.trace_add("write", self.actualizar_autocompletar)
        self.producto_var.trace_add("write", self.actualizar_autocompletar_productos)
        # Cargar datos de ejemplo
        self.cargar_clientes_desde_db()
        self.cargar_cuentas_desde_db()

    def buscar_descripcion(self):
        try:
            # Limpiar el Combobox antes de cargar nuevos valores
            self.producto_dropdown.set("")

            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Obtener la descripción ingresada
            descripcion_ingresada = self.descripcion_var.get().lower()

            # Construir la consulta SQL basada en la descripción
            consulta_sql = "SELECT referencia FROM productos"
            if descripcion_ingresada:
                consulta_sql += f" WHERE descripcion LIKE '%{descripcion_ingresada}%'"

            # Ejecutar la consulta SQL para obtener las referencias
            cursor.execute(consulta_sql)

            # Obtener todas las referencias
            productos = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar las referencias en el Combobox
            nuevos_productos = [producto[0] for producto in productos]
            self.producto_dropdown['values'] = nuevos_productos
            print(nuevos_productos)
            self.descripcion_var.set("")

        except sqlite3.Error as e:
            print(f"Error al cargar productos desde la base de datos: {e}")

    def actualizar_autocompletar_productos(self, *args):
        # Obtener la entrada del usuario
        entrada_usuario = self.producto_var.get().lower()

        # Filtrar la lista de productos basándose en la entrada del usuario
        productos_filtrados = [producto for producto in self.productos if entrada_usuario in producto.lower()]

        # Configurar los productos filtrados en el Combobox
        self.producto_dropdown['values'] = productos_filtrados if entrada_usuario else self.productos

    def actualizar_autocompletar(self, *args):
        # Obtener la entrada del usuario
        entrada_usuario = self.cliente_var.get().lower()

        # Filtrar la lista de proveedores basándose en la entrada del usuario
        clientes_filtrados = [cliente for cliente in self.proveedor_dropdown['values'] if
                                 entrada_usuario in cliente.lower()]

        # Configurar los proveedores filtrados en el Combobox
        self.proveedor_dropdown['values'] = clientes_filtrados if entrada_usuario else self.proveedor_dropdown[
            'values']

    def obtener_info_producto(self, nombre_producto):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener la cantidad y el precio_venta del producto
            cursor.execute("SELECT cantidad, precio_venta FROM productos WHERE referencia = ?", (nombre_producto,))

            # Obtener la cantidad y el precio_venta del producto
            info_producto = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            return info_producto if info_producto else (None, None)

        except sqlite3.Error as e:
            print(f"Error al obtener la información del producto desde la base de datos: {e}")
            return None, None

    def actualizar_info_en_entries(self, event):
        # Obtener el nombre del producto seleccionado en el Combobox
        nombre_producto = self.producto_var.get()

        # Obtener la información del producto desde la base de datos
        cantidad_producto, precio_producto = self.obtener_info_producto(nombre_producto)

        # Asociar la cantidad del producto a una nueva variable
        self.stock_producto_var.set(cantidad_producto)
        # Asociar el precio_venta del producto a una nueva variable
        self.precio_var.set(precio_producto)

    def actualizar_dropdown_cuentas(self, event):
        # Obtener el valor seleccionado en el Combobox de modo de pago
        modo_pago_seleccionado = self.modo_pago_dropdown.get()

        # Si el modo de pago es "Contado", activar el Combobox de cuentas
        if modo_pago_seleccionado == "Contado":
            self.label_cuenta.grid(row=9, column=4, padx=(90, 0))
            self.cuenta_dropdown.grid(row=9, column=4, padx=(290, 0))
        else:
            # Si no es "Contado", ocultar el Combobox de cuentas
            self.label_cuenta.grid_remove()
            self.cuenta_dropdown.grid_remove()

    def cargar_cuentas_desde_db(self):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener las cuentas
            cursor.execute("SELECT nombre_banco FROM bancos")

            # Obtener todos los nombres de bancos
            cuentas = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            self.cuentas = [cuenta[0] for cuenta in cuentas]
            self.cuenta_dropdown['values'] = self.cuentas

        except sqlite3.Error as e:
            print(f"Error al cargar cuentas desde la base de datos: {e}")

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
            self.proveedor_dropdown['values'] = clientes

        except sqlite3.Error as e:
            print(f"Error al cargar proveedores desde la base de datos: {e}")

    def obtener_id_producto(self, nombre_producto):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el ID del producto
            cursor.execute("SELECT id FROM productos WHERE referencia = ?", (nombre_producto,))

            # Obtener el ID del producto
            id_producto = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            return id_producto[0] if id_producto else None

        except sqlite3.Error as e:
            print(f"Error al obtener el ID del producto desde la base de datos: {e}")
            return None

    def obtener_id_proveedor(self, nombre_cliente):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el ID del proveedor
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (nombre_cliente,))

            # Obtener el ID del proveedor
            id_cliente = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            return id_cliente[0] if id_cliente else None

        except sqlite3.Error as e:
            print(f"Error al obtener el ID del proveedor desde la base de datos: {e}")
            return None

    def agregar(self):
        try:
            self.btn_agregar.grid()
            self.btn_eliminar.grid()
            self.label_modo_pago.grid()
            self.modo_pago_dropdown.grid()
            self.btn_finalizar_venta.grid()
            self.label_cuenta.grid()
            self.cuenta_dropdown.grid()

            # Obtener los valores de las variables de control
            numero_venta_val = self.numero_venta_actual  # Utilizar el nuevo número de compra
            producto_nombre = self.producto_var.get()  # Obtener el nombre del producto

            # Validar que no haya campos vacíos
            if not producto_nombre:
                tk.messagebox.showerror("Error", "Por favor, seleccione un producto.")
                return

            # Convertir a float la cantidad y el precio si no están vacíos
            cantidad_val = float(self.cantidad_var.get()) if self.cantidad_var.get() else None
            precio_val = float(self.precio_var.get()) if self.precio_var.get() else None

            # Validar que no haya campos vacíos
            if cantidad_val is None or precio_val is None:
                tk.messagebox.showerror("Error", "Por favor, complete los campos de cantidad y precio.")
                return

            # Obtener el ID del producto seleccionado desde la base de datos
            id_producto = self.obtener_id_producto(producto_nombre)

            # Validar que se haya seleccionado un producto válido
            if id_producto is None:
                tk.messagebox.showerror("Error", "Seleccione un producto válido.")
                return

            subtotal_val = cantidad_val * precio_val

            # Verificar si hay una compra activa
            if self.numero_venta_actual is not None:
                # Insertar los detalles de la compra utilizando el ID de la compra
                self.insertar_detalles_venta(numero_venta_val, id_producto, cantidad_val, precio_val)

                # Agregar el nuevo registro a la lista
                self.lista.insert('', 'end', values=(
                    producto_nombre, cantidad_val, precio_val, self.numero_venta_actual, subtotal_val))

                # Limpiar los campos de entrada después de agregar
                self.limpiar_producto()
                self.cargar_productos_desde_db()
                self.cargar_clientes_desde_db()
            else:
                print("Error: No hay una compra activa.")

        except ValueError as ve:
            print(f"Error al convertir valores: {ve}")

    def obtener_ultima_venta_visual(self):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el número de la última compra
            cursor.execute("SELECT MAX(id) FROM ventas")

            # Obtener el número de la última compra
            ultima_venta = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar el número de la última compra en la nueva variable
            if ultima_venta and ultima_venta[0] is not None:
                numero_venta = ultima_venta[0] + 1
            else:
                numero_venta = 1

            # Adornar el número con ceros a la izquierda y configurar la variable
            self.ultima_venta_visual.set(str(numero_venta).zfill(5))

            # Configurar el número de la última compra en el Entry
            self.numero_venta_actual.set(self.ultima_venta_visual.get())

        except sqlite3.Error as e:
            print(f"Error al obtener la última compra desde la base de datos: {e}")

    def insertar_venta(self):
        try:

            # Deshabilitar el botón al hacer clic en él
            self.btn_insertar_venta.config(state=tk.DISABLED)


            id_cliente = self.obtener_id_proveedor(self.cliente_var.get())
            if id_cliente is None:
                self.btn_insertar_venta.config(state=tk.ACTIVE)
                tk.messagebox.showerror("Error", "Por favor, seleccione un cliente.")
                return
            else:
                # Ocultar el dropdown de proveedores
                self.proveedor_dropdown.grid_remove()
                self.label_cliente.grid_remove()
                self.fecha_venta_entry.grid_remove()
                self.label_fecha_venta.grid_remove()

                self.producto_dropdown.grid()
                self.label_producto.grid()
                self.label_precio.grid()
                self.entry_precio.grid()
                self.label_cantidad.grid()
                self.entry_cantidad.grid()
                self.btn_agregar.grid()
                self.btn_eliminar.grid()
                self.label_stock.grid()
                self.entry_stock.grid()
                self.entry_descripcion.grid()
                self.label_descripcion.grid()
                self.btn_buscar_descripcion.grid()
                # Conectar a la base de datos
                self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
                cursor = self.conexion.cursor()

                # Obtener la fecha de compra
                fecha_venta = self.fecha_venta_var.get()

                # Verificar si la conexión está abierta
                if not self.conexion:
                    print("Error: La conexión a la base de datos está cerrada.")
                    return None

                # Realizar el INSERT en la tabla de compras
                cursor.execute(
                    "INSERT INTO ventas (fecha_venta, cliente_id) VALUES (?, ?)",
                    (fecha_venta, id_cliente)
                )
                id_venta = cursor.lastrowid  # Obtener el ID de la compra recién insertada

                # Obtener el número de compra recién insertado
                cursor.execute("SELECT id FROM ventas WHERE id = ?", (id_venta,))
                numero_venta = cursor.fetchone()

                # Almacenar el número de compra en la variable
                if numero_venta:
                    self.numero_venta_actual = numero_venta[0]

                # Confirmar la transacción
                self.conexion.commit()

                # Cerrar el cursor y la conexión
                cursor.close()
                self.cerrar_conexion()
                print("Compra insertada con éxito.")

                # Retornar el ID de la compra
                return id_venta



        except sqlite3.Error as e:
            print(f"Error al insertar compra en la base de datos: {e}")
            return None

    def insertar_detalles_venta(self, id_venta, id_producto, cantidad_val, precio_val):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Realizar el INSERT en la tabla de detalles_venta
            cursor.execute(
                "INSERT INTO detalles_venta (id_producto, cantidad_producto, precio_producto, id_venta, fecha_creacion) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (id_producto, cantidad_val, precio_val, id_venta)
            )

            # Confirmar la transacción
            self.conexion.commit()

            # Realizar el UPDATE en la tabla de productos
            cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
                           (cantidad_val, id_producto))

            # Confirmar la transacción
            self.conexion.commit()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            print("Detalles de venta insertados con éxito, y cantidad actualizada en productos.")

        except sqlite3.Error as e:
            print(f"Error al insertar detalles de venta en la base de datos: {e}")

    def activar_desactivar_widgets(self, estado):
        # Activa o desactiva los widgets según el estado proporcionado

        # Dropdown de producto
        if estado == "activar":
            self.producto_dropdown.config(state=tk.NORMAL)
            self.label_producto.config(state=tk.NORMAL)
            self.label_precio.config(state=tk.NORMAL)
            self.entry_precio.config(state=tk.NORMAL)
            self.label_cantidad.config(state=tk.NORMAL)
            self.entry_cantidad.config(state=tk.NORMAL)
        elif estado == "desactivar":
            self.producto_dropdown.config(state=tk.DISABLED)
            self.label_producto.config(state=tk.DISABLED)
            self.label_precio.config(state=tk.DISABLED)
            self.entry_precio.config(state=tk.DISABLED)
            self.label_cantidad.config(state=tk.DISABLED)
            self.entry_cantidad.config(state=tk.DISABLED)

    def finalizar_compra(self, id_venta):
        try:
            self.btn_insertar_venta.config(state=tk.ACTIVE)

            # Ocultar el dropdown de proveedores
            self.proveedor_dropdown.grid()
            self.label_cliente.grid()
            self.fecha_venta_entry.grid()
            self.label_fecha_venta.grid()

            self.producto_dropdown.grid_remove()
            self.label_producto.grid_remove()
            self.label_precio.grid_remove()
            self.entry_precio.grid_remove()
            self.label_cantidad.grid_remove()
            self.entry_cantidad.grid_remove()
            self.btn_agregar.grid_remove()
            self.btn_eliminar.grid_remove()
            self.btn_agregar.grid_remove()
            self.btn_eliminar.grid_remove()
            self.label_modo_pago.grid_remove()
            self.modo_pago_dropdown.grid_remove()
            self.btn_finalizar_venta.grid_remove()
            self.entry_stock.grid_remove()
            self.label_stock.grid_remove()
            self.entry_descripcion.grid_remove()
            self.label_descripcion.grid_remove()
            self.btn_buscar_descripcion.grid_remove()
            # Obtener el nombre del banco seleccionado
            nombre_banco_seleccionado = self.cuenta_var.get()

            # Obtener el ID del banco utilizando el método
            id_banco_seleccionado = self.obtener_id_banco_desde_nombre(nombre_banco_seleccionado)

            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Realizar la consulta para obtener el total de la compra
            cursor.execute("SELECT SUM(total) FROM detalles_venta WHERE id_venta = ?", (id_venta,))
            total_venta = cursor.fetchone()[0]
            # Obtener el modo de pago seleccionado
            modo_pago_seleccionado = self.modo_pago_dropdown.get()
            saldo_restante = total_venta if modo_pago_seleccionado == "Crédito" else 0
            cursor.execute(
                "UPDATE ventas SET total = ?, forma_pago_id = ?, estado_venta = ?, saldo_restante = ? WHERE id = ?",
                (total_venta, id_banco_seleccionado,
                 "Cancelada" if modo_pago_seleccionado == "Contado" else "Activa", saldo_restante, id_venta))

            if modo_pago_seleccionado == "Contado":
                # Actualizar el saldo en la tabla de bancos si se obtiene el ID del banco
                if id_banco_seleccionado is not None:
                    cursor.execute("UPDATE bancos SET saldo = saldo + ? WHERE id = ?",
                                   (total_venta, id_banco_seleccionado))
                    # Confirmar la transacción
                    self.conexion.commit()
                else:
                    print("No se pudo obtener el ID del banco seleccionado.")
            elif modo_pago_seleccionado == "Crédito":
                # Actualizar el saldo en la tabla de ventas_credito
                cursor.execute("UPDATE ventas_credito SET saldo = saldo + ? WHERE id = 1", (total_venta,))

                # Actualizar el saldo en la tabla de clientes
                id_cliente = self.obtener_id_cliente_desde_venta(id_venta)
                if id_cliente is not None:
                    cursor.execute("UPDATE clientes SET saldo = saldo + ? WHERE id_cliente = ?",
                                   (total_venta, id_cliente))
                    # Confirmar la transacción
                    self.conexion.commit()
                else:
                    print("No se pudo obtener el ID del cliente asociado a la venta.")
            else:
                print("Modo de pago no reconocido.")
            self.numero_venta_actual += 1
            self.ultima_venta_visual.set(str(self.numero_venta_actual).zfill(5))

            # Cerrar el cursor y la conexión
            self.conexion.commit()
            cursor.close()
            self.cerrar_conexion()
            self.limpiar_tabla_temporal()
            print("Compra finalizada con éxito.")

        except sqlite3.Error as e:
            print(f"Error al finalizar compra en la base de datos: {e}")

    def obtener_id_cliente_desde_venta(self, id_venta):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL SELECT para obtener el cliente_id asociado a la venta
            cursor.execute("SELECT cliente_id FROM ventas WHERE id = ?", (id_venta,))

            # Obtener el resultado de la consulta
            result = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

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

    def limpiar_tabla_temporal(self):
        try:
            self.label_cuenta.grid_remove()
            self.cuenta_dropdown.grid_remove()
            # Obtener todos los ítems de la tabla
            items = self.lista.get_children()

            # Eliminar cada ítem de la tabla
            for item in items:
                self.lista.delete(item)

            # Limpiar los campos de entrada después de eliminar
            self.limpiar_campos()

            print("Registros de la tabla temporal eliminados con éxito.")

        except Exception as e:
            print(f"Error al limpiar la tabla temporal: {e}")

    def finalizar_compra_independiente(self):
        try:
            # Obtener el número de compra actual
            numero_venta_actual = self.numero_venta_actual

            # Verificar si hay un número de compra válido
            if numero_venta_actual is not None:
                # Llamar al método finalizar_compra con el número de compra actual
                self.finalizar_compra(numero_venta_actual)
            else:
                print("Error: No se pudo obtener el número de compra actual.")
        except Exception as e:
            print(f"Error al finalizar compra de forma independiente: {e}")

    def eliminar(self):
        # Obtener el índice seleccionado en la lista
        seleccion = self.lista.selection()
        if seleccion:
            # Obtener los valores del registro seleccionado
            valores = self.lista.item(seleccion, 'values')

            # Obtener la referencia y el número de compra
            referencia_producto = valores[0]
            numero_venta = valores[3]  # Supongo que el número de compra está en la cuarta columna

            # Obtener el id_producto utilizando el método obtener_id_producto
            id_producto = self.obtener_id_producto(referencia_producto)

            if id_producto and numero_venta:
                # Mostrar la referencia, número de compra y el id_producto en la consola para depuración
                print(
                    f"Referencia a eliminar: {referencia_producto}, Número de Compra: {numero_venta}, ID Producto: {id_producto}")

                # Confirmar la eliminación con un cuadro de diálogo
                confirmar_eliminar = tk.messagebox.askyesno("Eliminar Registro",
                                                            f"¿Estás seguro de eliminar el registro con la siguiente referencia y número de venta?\n"
                                                            f"Referencia: {referencia_producto}, Número de Compra: {numero_venta}")

                if confirmar_eliminar:
                    try:
                        # Conectar a la base de datos
                        self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
                        cursor = self.conexion.cursor()

                        # Mostrar la sentencia DELETE en la consola para depuración
                        delete_query = "DELETE FROM detalles_venta WHERE id_producto = ? AND id_venta = ?"
                        print("Sentencia DELETE:", delete_query)

                        # Ejecutar la sentencia SQL DELETE
                        cursor.execute(delete_query, (id_producto, numero_venta))

                        # Confirmar la transacción
                        self.conexion.commit()

                        # Cerrar el cursor y la conexión
                        cursor.close()
                        self.cerrar_conexion()

                        # Eliminar el registro de la lista
                        self.lista.delete(seleccion)

                        # Limpiar los campos de entrada después de eliminar
                        self.limpiar_campos()

                        print("Registro eliminado con éxito.")

                    except sqlite3.Error as e:
                        print(f"Error al eliminar registro de la base de datos: {e}")
            else:
                print("Error: No se pudo obtener el ID del producto o el número de compra.")

    def cargar_registro_seleccionado(self, event):
        try:
            # Obtener el índice seleccionado en la lista
            seleccion = self.lista.selection()
            if seleccion:
                # Obtener los primeros cuatro valores del registro seleccionado
                valores = self.lista.item(seleccion, 'values')[:4]

        except Exception as e:
            print(f"Error al cargar registro seleccionado: {e}")

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.numero_venta_var.set('')
        self.cliente_var.set('')
        self.producto_var.set('')
        self.metodo_pago_var.set('')

    def limpiar_producto(self):
        self.precio_var.set(0)
        self.cantidad_var.set(0)
        self.producto_var.set('')

    def cargar_productos_desde_db(self):

        try:


            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener los productos
            cursor.execute("SELECT referencia FROM productos")

            # Obtener todos los productos
            productos = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar los productos en el Combobox
            self.productos = [producto[0] for producto in productos]

        except sqlite3.Error as e:
            print(f"Error al cargar productos desde la base de datos: {e}")

    def obtener_precio_producto(self, nombre_producto):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el precio_venta del producto
            cursor.execute("SELECT precio_venta FROM productos WHERE referencia = ?", (nombre_producto,))

            # Obtener el precio_venta del producto
            precio_producto = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            return precio_producto[0] if precio_producto else None

        except sqlite3.Error as e:
            print(f"Error al obtener el precio del producto desde la base de datos: {e}")
            return None

    def actualizar_precio_en_entry(self, event):
        # Obtener el nombre del producto seleccionado en el Combobox
        nombre_producto = self.producto_var.get()

        # Obtener el precio del producto desde la base de datos
        precio_producto = self.obtener_precio_producto(nombre_producto)

        # Asociar el precio del producto a una nueva variable
        self.precio_var.set(precio_producto)

    def obtener_id_banco_desde_combobox(self, event):
        try:
            # Obtener el nombre del banco seleccionado
            nombre_banco = self.cuenta_var.get()

            # Obtener el ID del banco utilizando el método existente
            id_banco = self.obtener_id_banco_desde_nombre(nombre_banco)

            if id_banco is not None:
                # Imprimir el ID del banco (puedes hacer lo que quieras con él)
                print(f"ID del banco seleccionado: {id_banco}")
            else:
                print("No se pudo obtener el ID del banco seleccionado.")

        except Exception as e:
            print(f"Error al obtener el ID del banco: {e}")

    def obtener_id_banco_desde_nombre(self, nombre_banco):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el ID del banco
            cursor.execute("SELECT id FROM bancos WHERE nombre_banco = ?", (nombre_banco,))

            # Obtener el ID del banco
            id_banco = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            return id_banco[0] if id_banco else None

        except sqlite3.Error as e:
            print(f"Error al obtener el ID del banco desde la base de datos: {e}")
            return None

    def cerrar(self):
        # Método para cerrar la ventana del CRUD
        self.destroy()

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

if __name__ == "__main__":
    root = tk.Tk()  # Cambiar a tk.Tk() en lugar de tk.Toplevel()
    app = VentaCRUD(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')  # No es necesario pasar None como main_content
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
