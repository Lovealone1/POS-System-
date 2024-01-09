import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from edit_producto import FormularioEnvio
from tkinter import filedialog
import openpyxl

class ProductoCRUD(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Variables de control
        self.id_var = tk.StringVar()
        self.referencia_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_compra_var = tk.StringVar()
        self.precio_venta_var = tk.StringVar()
        self.estado_var = tk.StringVar()

        # Etiquetas y campos de entrada
        self.label_referencia = tk.Label(master, text="Referencia:")
        self.label_referencia.grid(row=0, column=0, sticky="e", padx=(0, 5),
                                   pady=(5, 5))  # Ajusta pady según tus necesidades
        self.entry_referencia = tk.Entry(master, textvariable=self.referencia_var, width=22)
        self.entry_referencia.grid(row=0, column=1, padx=(0, 4), pady=(5, 5))  # Ajusta pady según tus necesidades

        self.label_descripcion = tk.Label(master, text="Descripción:")
        self.label_descripcion.grid(row=1, column=0, sticky="e", padx=(0, 5),
                                    pady=(0, 8))  # Ajusta pady según tus necesidades
        self.entry_descripcion = tk.Entry(master, textvariable=self.descripcion_var, width=22)
        self.entry_descripcion.grid(row=1, column=1, padx=(0, 4), pady=(0, 8))

        self.label_cantidad = tk.Label(master, text="Cantidad:")
        self.label_cantidad.grid(row=2,column=0, sticky="e", padx=(0, 5),
                                    pady=(0, 10))
        self.entry_cantidad = tk.Entry(master, textvariable=self.cantidad_var, width=22)
        self.entry_cantidad.grid(row=2, column=1, padx=(0, 4))

        self.label_precio_compra = tk.Label(master, text="Precio de Compra:")
        self.label_precio_compra.grid(row=3, column=0, sticky="e", padx=(0, 5),
                                    pady=(0, 12))
        self.entry_precio_compra = tk.Entry(master, textvariable=self.precio_compra_var, width=22)
        self.entry_precio_compra.grid(row=3, column=1, padx=(0, 4))

        self.label_precio_venta = tk.Label(master, text="Precio de Venta:")
        self.label_precio_venta.grid(row=4, column=0, sticky="e", padx=(0, 5),
                                    pady=(5, 12))
        self.entry_precio_venta = tk.Entry(master, textvariable=self.precio_venta_var, width=22)
        self.entry_precio_venta.grid(row=4, column=1, padx=(0, 4))

        # Agregar espacio a la derecha entre los input texts y la tabla
        self.lista = ttk.Treeview(master, columns=(
            'Id', 'Referencia', 'Descripción', 'Cantidad', 'Precio de Compra', 'Precio de Venta', 'Estado'),
                                  show='headings')
        self.lista.grid(row=0, rowspan=8, column=2, columnspan=4, pady=0, padx=(10, 20))
        self.lista.heading('Id', text='Id')
        self.lista.heading('Referencia', text='Referencia')
        self.lista.heading('Descripción', text='Descripción')
        self.lista.heading('Cantidad', text='Cantidad')
        self.lista.heading('Precio de Compra', text='Precio de Compra')
        self.lista.heading('Precio de Venta', text='Precio de Venta')
        self.lista.heading('Estado', text='Estado')

        # Ajustar el tamaño de las columnas
        self.lista.column('Id', width=40)  # Puedes ajustar el valor según tus necesidades
        self.lista.column('Referencia', width=100)
        self.lista.column('Descripción', width=150)
        self.lista.column('Cantidad', width=80)
        self.lista.column('Precio de Compra', width=120)
        self.lista.column('Precio de Venta', width=120)
        self.lista.column('Estado', width=80)

        # Etiqueta y Combobox
        self.label_estado = tk.Label(master, text="Estado:")
        self.label_estado.grid(row=5, column=0, sticky="e")

        # Agrega "Seleccione" como el primer elemento en las opciones
        self.estado_options = ["Activo", "Inactivo"]
        self.estado_dropdown = ttk.Combobox(master, textvariable=self.estado_var, values=self.estado_options, width=19,
                                            state="readonly")
        self.estado_dropdown.grid(row=5, column=1)

        # Configura el valor inicial del Combobox como "Seleccione"
        self.estado_dropdown.set("Seleccione")

        # Vincula el evento <<ComboboxSelected>> para manejar la selección
        self.estado_dropdown.bind("<<ComboboxSelected>>", self.handle_combobox_selection)

        # Botones
        self.btn_agregar = tk.Button(master, text="Agregar", command=self.agregar)
        self.btn_agregar.grid(row=6, column=0, columnspan=2, pady=10, padx=(80, 0))

        self.btn_actualizar = tk.Button(master, text="Actualizar", command=self.abrir_editar_producto, bg="#CCFFFF")
        self.btn_actualizar.grid(row=9, column=5, pady=5, columnspan=2, padx=(0, 70), sticky='e')

        self.btn_eliminar = tk.Button(master, text="Eliminar", command=lambda: self.eliminar(self.lista.selection()), bg="#FF9999")
        self.btn_eliminar.grid(row=9, column=5, pady=5, columnspan=2, padx=(0, 10), sticky='e')

        self.btn_bulk_insert = tk.Button(master, text="Cargar productos XL", command=self.bulk_insert_desde_excel)
        self.btn_bulk_insert.grid(row=9, column=0, pady=5, columnspan=2, padx=(50, 0), sticky='w')

        self.rld = tk.Button(master, text="↻", command=self.actualizar_tabla)
        self.rld.grid(row=9, column=0, pady=5, columnspan=2, padx=(20, 0), sticky='w')

        # Evento de selección de la lista
        self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
        # Cargar datos de ejemplo
        self.cargar_datos_desde_db()

    def actualizar_tabla(self):
        # Método para actualizar la tabla de compras
        self.lista.delete(*self.lista.get_children())
        self.cargar_datos_desde_db()

    def abrir_editar_producto(self):
        # Obtener el índice seleccionado en la lista
        seleccion = self.lista.selection()
        if not seleccion:
            tk.messagebox.showinfo("Información", "Por favor, seleccione un producto.")
            return

        # Obtener los valores del producto seleccionado
        id_producto_seleccionado = self.lista.item(seleccion, 'values')[0]
        referencia_val = self.lista.item(seleccion, 'values')[1]
        descripcion_val = self.lista.item(seleccion, 'values')[2]
        cantidad_val = self.lista.item(seleccion, 'values')[3]
        precio_compra_val = self.lista.item(seleccion, 'values')[4]
        precio_venta_val = self.lista.item(seleccion, 'values')[5]
        estado_val = self.lista.item(seleccion, 'values')[6]

        # Crear una nueva ventana emergente (Toplevel)
        ventana_edicion = tk.Toplevel(self)

        # Crear una instancia de FormularioEnvio en la nueva ventana
        formulario_envio = FormularioEnvio(ventana_edicion)
        formulario_envio.id_var.set(id_producto_seleccionado)
        formulario_envio.referencia_var.set(referencia_val)
        formulario_envio.descripcion_var.set(descripcion_val)
        formulario_envio.cantidad_var.set(cantidad_val)
        formulario_envio.precio_compra_var.set(precio_compra_val)
        formulario_envio.precio_venta_var.set(precio_venta_val)
        formulario_envio.estado_var.set(estado_val)

        # Mostrar la ventana de edición
        formulario_envio.mostrar_ventana()

    def handle_combobox_selection(self, event):
        # Obtiene el valor seleccionado actual
        selected_value = self.estado_var.get()

        # Si el valor seleccionado es "Seleccione", muestra un mensaje de error
        if selected_value == "Seleccione":
            tk.messagebox.showerror("Error", "Por favor, selecciona un estado válido.")

    def cargar_datos_desde_db(self):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL SELECT para obtener todos los clientes
            cursor.execute("SELECT * FROM productos")

            # Obtener todos los registros
            registros = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            # Limpiar la lista antes de cargar los nuevos datos
            self.lista.delete(*self.lista.get_children())

            # Cargar los datos en la lista
            for registro in registros:
                self.lista.insert('', 'end', values=registro)

        except sqlite3.Error as e:
            print(f"Error al cargar datos desde la base de datos: {e}")

    def agregar(self):
        # Obtener los valores de las variables de control
        referencia_val = self.referencia_var.get()
        descripcion_val = self.descripcion_var.get()
        cantidad_val = self.cantidad_var.get()
        precio_compra_val = self.precio_compra_var.get()
        precio_venta_val = self.precio_venta_var.get()
        estado_val = self.estado_var.get()

        # Validar que no haya campos vacíos
        if not referencia_val or not descripcion_val or not cantidad_val or not precio_compra_val or not precio_venta_val or not estado_val:
            tk.messagebox.showerror("Error", "Todos los campos deben ser completados.")
            return

        # Validar que la cantidad sea un número entero positivo
        try:
            cantidad_val = int(cantidad_val)
            if cantidad_val < 0:
                raise ValueError("La cantidad debe ser un número entero positivo.")
        except ValueError:
            tk.messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        # Validar que los precios sean números positivos
        try:
            precio_compra_val = float(precio_compra_val)
            precio_venta_val = float(precio_venta_val)
            if precio_compra_val < 0 or precio_venta_val < 0:
                raise ValueError("Los precios deben ser números positivos.")
        except ValueError:
            tk.messagebox.showerror("Error", "Los precios deben ser números positivos.")
            return

        if estado_val == "Seleccione":
            tk.messagebox.showerror("Error", "Por favor, selecciona un estado válido.")
            return

        # Verificar si ya existe un producto con la misma referencia
        if self.existe_producto(referencia_val):
            tk.messagebox.showerror("Error", "Ya existe un producto con la misma referencia.")
            return

        # Agregar el nuevo registro a la lista
        self.lista.insert('', 'end', values=(
            referencia_val, descripcion_val, cantidad_val, precio_compra_val, precio_venta_val, estado_val))

        # Insertar en la base de datos
        self.insertar_producto_en_db(referencia_val, descripcion_val, cantidad_val, precio_compra_val, precio_venta_val,
                                     estado_val)

        # Limpiar los campos de entrada después de agregar
        self.limpiar_campos()

    def actualizar(self):
        # Obtener el índice seleccionado en la lista
        seleccion = self.lista.selection()
        if seleccion:
            # Obtener los nuevos valores de las variables de control
            referencia_val = self.referencia_var.get()
            descripcion_val = self.descripcion_var.get()
            cantidad_val = self.cantidad_var.get()
            precio_compra_val = self.precio_compra_var.get()
            precio_venta_val = self.precio_venta_var.get()
            estado_val = self.estado_var.get()

            # Actualizar el registro en la lista
            self.lista.item(seleccion, values=(referencia_val, descripcion_val, cantidad_val, precio_compra_val, precio_venta_val, estado_val))

            # Limpiar los campos de entrada después de actualizar
            self.limpiar_campos()
            self.cargar_datos_desde_db()

    def eliminar(self, item):
        # Obtener el id_producto seleccionado en la lista
        id_producto_seleccionado = self.lista.item(item, 'values')[0]

        if id_producto_seleccionado:
            confirmar_eliminar = tk.messagebox.askyesno("Eliminar Registro",
                                                        f"¿Estás seguro de eliminar el producto con ID Producto {id_producto_seleccionado}?")

            if confirmar_eliminar:
                # Lógica para eliminar el registro de la base de datos
                try:
                    # Crear un cursor
                    cursor = self.conexion.cursor()

                    # Ejecutar la sentencia SQL DELETE
                    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto_seleccionado,))

                    # Confirmar la transacción
                    self.conexion.commit()

                    # Cerrar el cursor
                    cursor.close()

                    # Eliminar el registro de la lista
                    self.lista.delete(item)

                    # Limpiar los campos de entrada después de eliminar
                    self.limpiar_campos()

                except sqlite3.Error as e:
                    print(f"Error al eliminar producto de la base de datos: {e}")

    def bulk_insert_desde_excel(self):
        # Abrir el cuadro de diálogo para seleccionar el archivo Excel
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        # Validar si se seleccionó un archivo
        if not file_path:
            return

        try:
            # Abrir el archivo Excel
            workbook = openpyxl.load_workbook(file_path)

            # Seleccionar la hoja de trabajo (asumiendo que es la primera hoja)
            sheet = workbook.active

            # Recorrer las filas de la hoja de trabajo
            for row_number, row in enumerate(sheet.iter_rows(min_row=2, values_only=True),
                                             start=2):  # Ignorar la primera fila (encabezados)
                # Tomar solo las primeras 5 columnas
                referencia, descripcion, cantidad, precio_compra, precio_venta = row[:5]

                # Asegurarse de que hay 5 valores en la fila
                if len(row) == 5:
                    # Llamar a la función para insertar en la base de datos sin proporcionar el estado
                    self.insertar_producto_en_db(referencia, descripcion, cantidad, precio_compra, precio_venta, "Activo")

                else:
                    print(
                        f"Error: Se esperaban 5 valores, pero se encontraron {len(row)} valores en la fila {row_number}.")
                    print(f"Valores en la fila {row_number}: {row[:5]}")

            # Cerrar el archivo Excel después de leer
            workbook.close()

            # Actualizar la tabla después de realizar el bulk insert
            self.cargar_datos_desde_db()

        except Exception as e:
            print(f"Error al procesar el archivo Excel: {e}")

    def insertar_producto_en_db(self, referencia, descripcion, cantidad, precio_compra, precio_venta, estado):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL INSERT
            cursor.execute(
                "INSERT INTO productos (referencia, descripcion, cantidad, precio_compra, precio_venta, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (referencia, descripcion, cantidad, precio_compra, precio_venta, estado))

            # Confirmar la transacción
            self.conexion.commit()

            # Cerrar el cursor
            cursor.close()

        except sqlite3.Error as e:
            print(f"Error al insertar producto en la base de datos: {e}")

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.referencia_var.set('')
        self.descripcion_var.set('')
        self.cantidad_var.set('')
        self.precio_compra_var.set('')
        self.precio_venta_var.set('')
        self.estado_var.set('')

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

    def existe_producto(self, referencia):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL SELECT para verificar si ya existe un producto con la misma referencia
            cursor.execute("SELECT * FROM productos WHERE referencia = ?", (referencia,))

            # Obtener el primer registro (si existe)
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro is not None

        except sqlite3.Error as e:
            print(f"Error al verificar si existe el producto en la base de datos: {e}")
            return False

if __name__ == "__main__":
    root = tk.Tk()  # Cambiar a tk.Tk() en lugar de tk.Toplevel()
    app = ProductoCRUD(root)  # Pasar None como main_content
    root.geometry("960x325")
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()