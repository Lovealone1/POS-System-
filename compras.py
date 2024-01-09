import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from tkinter import messagebox
class CrudCompras(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ventana de Compras")

        # Variables de control
        self.numero_compra_var = tk.StringVar()
        self.proveedor_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.metodo_pago_var = tk.StringVar()
        self.precio_var = tk.DoubleVar()
        self.cantidad_var = tk.DoubleVar()
        self.numero_compra_actual = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.label_proveedor = tk.Label(self, text="Proveedor:")
        self.label_proveedor.grid(row=1, column=0, sticky="e")

        self.ultima_compra_visual = tk.StringVar()
        self.obtener_ultima_compra_visual()

        # Simulamos una lista de proveedores para el ejemplo
        proveedores = []
        self.proveedor_dropdown = ttk.Combobox(self, textvariable=self.proveedor_var, values=proveedores, width=15)
        self.proveedor_dropdown.grid(row=1, column=1)

        self.label_producto = tk.Label(self, text="Producto:")
        self.label_producto.grid(row=3, column=0, sticky="e",pady=(0,10))
        # Cargar productos desde la base de datos
        self.cargar_productos_desde_db()
        print(self.numero_compra_actual)
        self.label_fecha_compra = tk.Label(self, text="Fecha de Compra:")
        self.label_fecha_compra.grid(row=2, column=0, sticky="e")

        # Utilizar el widget DateEntry para seleccionar la fecha
        self.fecha_compra_var = tk.StringVar()
        self.fecha_compra_entry = DateEntry(self, textvariable=self.fecha_compra_var, date_pattern='dd/MM/yyyy')
        self.fecha_compra_entry.grid(row=2, column=1)

        self.label_descripcion = tk.Label(self, text="Descripción:")
        self.label_descripcion.grid(row=1, column=0, sticky="e")
        self.entry_descripcion = tk.Entry(self, textvariable=self.descripcion_var,width=10)
        self.entry_descripcion.grid(row=1, column=1,padx=(0,30))
        self.btn_buscar_descripcion = tk.Button(self, text="Filtrar", command=self.buscar_descripcion)
        self.btn_buscar_descripcion.grid(row=1, column=1,padx=(90,0))
        # Usar un Combobox para seleccionar el producto
        self.producto_dropdown = ttk.Combobox(self, textvariable=self.producto_var, values=self.productos, width=17)
        self.producto_dropdown.grid(row=3, column=1,pady=(0,10))

        self.entry_numero_compra = tk.Entry(self, textvariable=self.ultima_compra_visual, state="readonly")
        self.entry_numero_compra.grid(row=0, column=1, padx=(0, 0))

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
        self.entry_descripcion.grid_remove()
        self.label_descripcion.grid_remove()
        self.btn_buscar_descripcion.grid_remove()
        self.btn_buscar_descripcion.grid_remove()


        self.btn_insertar_compra = tk.Button(self, text="Generar Compra", command=self.insertar_compra)
        self.btn_insertar_compra.grid(row=0, column=0, columnspan=2, pady=10, padx=(0, 140))

        self.btn_agregar = tk.Button(self, text="Agregar producto", command=self.agregar)
        self.btn_agregar.grid(row=9, column=0, columnspan=2, padx=(170, 0), pady=10)

        self.btn_finalizar_compra = tk.Button(self, text="Finalizar Compra", command=self.finalizar_compra_independiente)
        self.btn_finalizar_compra.grid(row=9, column=5, pady=5, columnspan=1, padx=(0, 30), sticky='e')

        self.btn_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar)
        self.btn_eliminar.grid(row=9, column=0, columnspan=2, pady=10)

        self.lista = ttk.Treeview(self, columns=('ID Producto', 'Cantidad', 'Precio', 'ID Compra'),
                                  show='headings')
        self.lista.grid(row=0, rowspan=8, column=2, columnspan=4, pady=10, padx=(20,20))
        self.lista.heading('ID Producto', text='ID Producto')
        self.lista.heading('Cantidad', text='Cantidad')
        self.lista.heading('Precio', text='Precio')
        self.lista.heading('ID Compra', text='ID Compra')
        self.lista.column('ID Producto', width=100, anchor=tk.CENTER)
        self.lista.column('Cantidad', width=100, anchor=tk.CENTER)
        self.lista.column('Precio', width=100, anchor=tk.CENTER)
        self.lista.column('ID Compra', width=100, anchor=tk.CENTER)
        self.label_modo_pago = tk.Label(self, text="Modo de Pago:")
        self.label_modo_pago.grid(row=9, column=5,padx=(0,286))
        modos_pago = ["Crédito", "Contado"]
        self.modo_pago_dropdown = ttk.Combobox(self, textvariable=self.metodo_pago_var, values=modos_pago)
        self.modo_pago_dropdown.grid(row=9, column=5,padx=(0, 50))
        self.label_cuenta = tk.Label(self, text="Cuenta:")
        self.label_cuenta.grid(row=9, column=4, padx=(90, 0))
        self.cuenta_var = tk.StringVar()
        cuentas = []
        self.cuenta_dropdown = ttk.Combobox(self, textvariable=self.cuenta_var, values=cuentas)
        self.cuenta_dropdown.grid(row=9, column=4, padx=(290, 0))

        self.label_cuenta.grid_remove()
        self.cuenta_dropdown.grid_remove()

        self.btn_agregar.grid_remove()
        self.btn_eliminar.grid_remove()
        self.label_modo_pago.grid_remove()
        self.modo_pago_dropdown.grid_remove()
        self.btn_finalizar_compra.grid_remove()
        self.label_cuenta.grid_remove()
        self.cuenta_dropdown.grid_remove()


        # Evento de selección de la lista
        self.lista.bind('<ButtonRelease-1>', self.cargar_registro_seleccionado)
        self.producto_dropdown.bind("<<ComboboxSelected>>", self.obtener_precio_seleccionado)
        self.cuenta_dropdown.bind("<<ComboboxSelected>>", self.obtener_id_banco_desde_combobox)
        self.modo_pago_dropdown.bind("<<ComboboxSelected>>", self.actualizar_dropdown_cuentas)

        # Configurar el evento para autocompletar al escribir

        # Asociar el evento KeyRelease al método autocompletar_proveedores
        self.proveedor_var.trace_add("write", self.actualizar_autocompletar)
        self.producto_var.trace_add("write", self.actualizar_autocompletar_productos)



        # Cargar datos de ejemplo
        self.cargar_proveedores_desde_db()
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
        entrada_usuario = self.proveedor_var.get().lower()

        # Filtrar la lista de proveedores basándose en la entrada del usuario
        proveedores_filtrados = [proveedor for proveedor in self.proveedor_dropdown['values'] if
                                 entrada_usuario in proveedor.lower()]

        # Configurar los proveedores filtrados en el Combobox
        self.proveedor_dropdown['values'] = proveedores_filtrados if entrada_usuario else self.proveedor_dropdown[
            'values']

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

    def cargar_proveedores_desde_db(self):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener los proveedores
            cursor.execute("SELECT nombre FROM proveedores")

            # Obtener todos los proveedores y almacenarlos como una variable local
            lista_proveedores = [proveedor[0] for proveedor in cursor.fetchall()]

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar los proveedores en el Combobox
            self.proveedor_dropdown['values'] = lista_proveedores

            # Asegurarse de invocar al método de autocompletar después de cargar los proveedores

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

    def obtener_id_proveedor(self, nombre_proveedor):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el ID del proveedor
            cursor.execute("SELECT id_proveedor FROM proveedores WHERE nombre = ?", (nombre_proveedor,))

            # Obtener el ID del proveedor
            id_proveedor = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            return id_proveedor[0] if id_proveedor else None

        except sqlite3.Error as e:
            print(f"Error al obtener el ID del proveedor desde la base de datos: {e}")
            return None

    def agregar(self):

        try:
            self.btn_agregar.grid()
            self.btn_eliminar.grid()
            self.label_modo_pago.grid()
            self.modo_pago_dropdown.grid()
            self.btn_finalizar_compra.grid()
            self.label_cuenta.grid()
            self.cuenta_dropdown.grid()
            # Obtener los valores de las variables de control
            numero_compra_val = self.numero_compra_actual  # Utilizar el nuevo número de compra
            producto_nombre = self.producto_var.get()  # Obtener el nombre del producto
            cantidad_val = float(self.cantidad_var.get())  # Convertir a float la cantidad
            precio_val = float(self.precio_var.get())  # Convertir a float el precio

            # Obtener el ID del producto seleccionado desde la base de datos
            id_producto = self.obtener_id_producto(producto_nombre)

            # Insertar la compra y obtener el ID de la compra recién insertada
            # Verificar si hay una compra activa
            if self.numero_compra_actual is not None:
                # Insertar los detalles de la compra utilizando el ID de la compra
                self.insertar_detalles_compra(numero_compra_val, id_producto, cantidad_val, precio_val)

                # Agregar el nuevo registro a la lista
                self.lista.insert('', 'end',
                                  values=(producto_nombre, cantidad_val, precio_val, self.numero_compra_actual))

                # Limpiar los campos de entrada después de agregar
                self.limpiar_producto()
                self.cargar_productos_desde_db()
            else:
                print("Error: No hay una compra activa.")


        except ValueError as ve:
            print(f"Error al convertir valores: {ve}")

    def obtener_ultima_compra_visual(self):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener el número de la última compra
            cursor.execute("SELECT MAX(id) FROM compras")

            # Obtener el número de la última compra
            ultima_compra = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar el número de la última compra en la nueva variable
            if ultima_compra and ultima_compra[0] is not None:
                numero_compra = ultima_compra[0] + 1
            else:
                numero_compra = 1

            # Adornar el número con ceros a la izquierda y configurar la variable
            self.ultima_compra_visual.set(str(numero_compra).zfill(5))

            # Configurar el número de la última compra en el Entry
            self.numero_compra_actual.set(self.ultima_compra_visual.get())

        except sqlite3.Error as e:
            print(f"Error al obtener la última compra desde la base de datos: {e}")

    def insertar_compra(self):
        try:

            # Deshabilitar el botón al hacer clic en él
            self.btn_insertar_compra.config(state=tk.DISABLED)
            id_proveedor = self.obtener_id_proveedor(self.proveedor_var.get())
            if id_proveedor is None:
                tk.messagebox.showerror("Error", "Por favor, seleccione un proveedor.")
                self.btn_insertar_compra.config(state=tk.ACTIVE)
                return
            else:
                self.proveedor_dropdown.grid_remove()
                self.label_proveedor.grid_remove()
                self.fecha_compra_entry.grid_remove()
                self.label_fecha_compra.grid_remove()

                self.producto_dropdown.grid()
                self.label_producto.grid()
                self.label_precio.grid()
                self.entry_precio.grid()
                self.label_cantidad.grid()
                self.entry_cantidad.grid()
                self.btn_agregar.grid()
                self.btn_eliminar.grid()
                self.label_descripcion.grid()
                self.entry_descripcion.grid()
                self.btn_buscar_descripcion.grid()
                self.btn_buscar_descripcion.grid()

                # Conectar a la base de datos
                self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
                cursor = self.conexion.cursor()

                # Obtener la fecha de compra
                fecha_compra = self.fecha_compra_var.get()

                # Verificar si la conexión está abierta
                if not self.conexion:
                    print("Error: La conexión a la base de datos está cerrada.")
                    return None

                # Realizar el INSERT en la tabla de compras
                cursor.execute(
                    "INSERT INTO compras (fecha_compra, proveedor_id) VALUES (?, ?)",
                    (fecha_compra, id_proveedor)
                )
                id_compra = cursor.lastrowid  # Obtener el ID de la compra recién insertada

                # Obtener el número de compra recién insertado
                cursor.execute("SELECT id FROM compras WHERE id = ?", (id_compra,))
                numero_compra = cursor.fetchone()

                # Almacenar el número de compra en la variable
                if numero_compra:
                    self.numero_compra_actual = numero_compra[0]

                # Confirmar la transacción
                self.conexion.commit()

                # Cerrar el cursor y la conexión
                cursor.close()
                self.cerrar_conexion()
                print("Compra insertada con éxito.")

                # Retornar el ID de la compra
                return id_compra


        except sqlite3.Error as e:
            print(f"Error al insertar compra en la base de datos: {e}")
            return None

    def insertar_detalles_compra(self, id_compra, id_producto, cantidad_val, precio_val):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Realizar el INSERT en la tabla de detalles_compra
            cursor.execute(
                "INSERT INTO detalles_compra (id_producto, cantidad_producto, precio_producto, id_compra, fecha_creacion) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (id_producto, cantidad_val, precio_val, id_compra)
            )

            # Confirmar la transacción
            self.conexion.commit()

            # Realizar el UPDATE en la tabla de productos
            cursor.execute("UPDATE productos SET cantidad = cantidad + ?, precio_compra = ? WHERE id = ?",
                           (cantidad_val, precio_val, id_producto))

            # Confirmar la transacción
            self.conexion.commit()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            print("Detalles de compra insertados con éxito, y cantidad y precio_compra actualizados en productos.")

        except sqlite3.Error as e:
            print(f"Error al insertar detalles de compra en la base de datos: {e}")

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

    def finalizar_compra(self, id_compra):
        try:
            self.btn_insertar_compra.config(state=tk.ACTIVE)

            # Ocultar el dropdown de proveedores
            self.proveedor_dropdown.grid()
            self.label_proveedor.grid()
            self.fecha_compra_entry.grid()
            self.label_fecha_compra.grid()
            self.producto_dropdown.grid()

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
            self.btn_finalizar_compra.grid_remove()
            self.entry_descripcion.grid_remove()
            self.label_descripcion.grid_remove()
            self.btn_buscar_descripcion.grid_remove()
            self.btn_buscar_descripcion.grid_remove()

            # Obtener el nombre del banco seleccionado
            nombre_banco_seleccionado = self.cuenta_var.get()

            # Obtener el ID del banco utilizando el método
            id_banco_seleccionado = self.obtener_id_banco_desde_nombre(nombre_banco_seleccionado)

            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Realizar la consulta para obtener el total de la compra
            cursor.execute("SELECT SUM(total) FROM detalles_compra WHERE id_compra = ?", (id_compra,))
            total_compra = cursor.fetchone()[0]

            # Obtener el modo de pago seleccionado
            modo_pago_seleccionado = self.modo_pago_dropdown.get()
            saldo_restante = total_compra if modo_pago_seleccionado == "Crédito" else 0
            cursor.execute(
                "UPDATE compras SET total = ?, forma_pago_id = ?, estado_compra = ?, saldo_restante = ? WHERE id = ?",
                (total_compra, id_banco_seleccionado,
                 "Cancelada" if modo_pago_seleccionado == "Contado" else "Activa", saldo_restante, id_compra))

            if modo_pago_seleccionado == "Contado":
                # Actualizar el saldo en la tabla de bancos si se obtiene el ID del banco
                if id_banco_seleccionado is not None:
                    cursor.execute("UPDATE bancos SET saldo = saldo - ? WHERE id = ?",
                                   (total_compra, id_banco_seleccionado))
                    # Confirmar la transacción
                    self.conexion.commit()
                else:
                    print("No se pudo obtener el ID del banco seleccionado.")
            elif modo_pago_seleccionado == "Crédito":
                # Actualizar el saldo en la tabla de compras_credito
                cursor.execute("UPDATE compras_credito SET saldo = saldo + ? WHERE id = 1",
                               (total_compra,))
                # Confirmar la transacción
                self.conexion.commit()
            else:
                print("Modo de pago no reconocido.")

            self.numero_compra_actual += 1
            self.ultima_compra_visual.set(str(self.numero_compra_actual).zfill(5))

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()
            self.limpiar_tabla_temporal()
            print("Compra finalizada con éxito.")

        except sqlite3.Error as e:
            print(f"Error al finalizar compra en la base de datos: {e}")

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
            numero_compra_actual = self.numero_compra_actual

            # Verificar si hay un número de compra válido
            if numero_compra_actual is not None:
                # Llamar al método finalizar_compra con el número de compra actual
                self.finalizar_compra(numero_compra_actual)
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
            numero_compra = valores[3]  # Supongo que el número de compra está en la cuarta columna

            # Obtener el id_producto utilizando el método obtener_id_producto
            id_producto = self.obtener_id_producto(referencia_producto)

            if id_producto and numero_compra:
                # Mostrar la referencia, número de compra y el id_producto en la consola para depuración
                print(
                    f"Referencia a eliminar: {referencia_producto}, Número de Compra: {numero_compra}, ID Producto: {id_producto}")

                # Confirmar la eliminación con un cuadro de diálogo
                confirmar_eliminar = tk.messagebox.askyesno("Eliminar Registro",
                                                            f"¿Estás seguro de eliminar el registro con la siguiente referencia y número de compra?\n"
                                                            f"Referencia: {referencia_producto}, Número de Compra: {numero_compra}")

                if confirmar_eliminar:
                    try:
                        # Conectar a la base de datos
                        self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
                        cursor = self.conexion.cursor()

                        # Mostrar la sentencia DELETE en la consola para depuración
                        delete_query = "DELETE FROM detalles_compra WHERE id_producto = ? AND id_compra = ?"
                        print("Sentencia DELETE:", delete_query)

                        # Ejecutar la sentencia SQL DELETE
                        cursor.execute(delete_query, (id_producto, numero_compra))

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
        self.numero_compra_var.set('')
        self.proveedor_var.set('')
        self.producto_var.set('')
        self.metodo_pago_var.set('')

    def limpiar_producto(self):
        self.precio_var.set(0)
        self.cantidad_var.set(0)
        self.producto_var.set('')

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

    def cargar_productos_desde_db(self):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Ejecutar la consulta SQL para obtener los productos
            cursor.execute("SELECT referencia FROM productos")

            # Obtener todas las referencias y descripciones
            productos = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar las referencias en el Combobox
            self.productos = [producto[0] for producto in productos]

            # Configurar las descripciones en una nueva lista

        except sqlite3.Error as e:
            print(f"Error al cargar productos desde la base de datos: {e}")

    def obtener_precio_seleccionado(self,event=None):
        try:
            # Conectar a la base de datos
            self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = self.conexion.cursor()

            # Obtener la referencia del producto seleccionado
            referencia_producto = self.producto_var.get()
            # Ejecutar la consulta SQL para obtener el precio_venta del producto
            cursor.execute("SELECT precio_venta FROM productos WHERE referencia = ?", (referencia_producto,))

            # Obtener el precio_venta del producto
            precio_producto = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            self.cerrar_conexion()

            # Configurar el precio en la variable de control y la etiqueta
            if precio_producto:
                self.precio_var.set(float(precio_producto[0]))
            else:
                self.precio_var.set(0.0)

        except sqlite3.Error as e:
            print(f"Error al obtener el precio del producto desde la base de datos: {e}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudCompras(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
