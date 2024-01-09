import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
from tkinter import messagebox
from edit_proveedor import FormularioEnvio
import openpyxl
class ProveedorCRUD(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Variables de control
        self.id_var = tk.StringVar()
        self.cc_nit_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.celular_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.ciudad_var = tk.StringVar()

        # Etiquetas y campos de entrada
        self.label_cc_nit = tk.Label(master, text="CC/NIT:")
        self.label_cc_nit.grid(row=0, column=0, sticky="e",pady=(10, 0))
        self.entry_cc_nit = tk.Entry(master, textvariable=self.cc_nit_var)
        self.entry_cc_nit.grid(row=0, column=1,pady=(10, 0))

        self.label_nombre = tk.Label(master, text="Nombre:")
        self.label_nombre.grid(row=1, column=0, sticky="e",pady=(0, 185))
        self.entry_nombre = tk.Entry(master, textvariable=self.nombre_var)
        self.entry_nombre.grid(row=1, column=1,pady=(0, 185))

        self.label_direccion = tk.Label(master, text="Dirección:")
        self.label_direccion.grid(row=1, column=0, sticky="e",pady=(0, 135))
        self.entry_direccion = tk.Entry(master, textvariable=self.direccion_var)
        self.entry_direccion.grid(row=1, column=1,pady=(0, 135))

        self.label_celular = tk.Label(master, text="Celular:")
        self.label_celular.grid(row=1, column=0, sticky="e",pady=(0, 85))
        self.entry_celular = tk.Entry(master, textvariable=self.celular_var)
        self.entry_celular.grid(row=1, column=1,pady=(0, 85))

        self.label_correo = tk.Label(master, text="Correo:")
        self.label_correo.grid(row=1, column=0, sticky="e",pady=(0, 35))
        self.entry_correo = tk.Entry(master, textvariable=self.correo_var)
        self.entry_correo.grid(row=1, column=1,pady=(0, 35))

        self.label_ciudad = tk.Label(master, text="Ciudad:")
        self.label_ciudad.grid(row=1, column=0, sticky="e",pady=(20, 0))
        self.entry_ciudad = tk.Entry(master, textvariable=self.ciudad_var)
        self.entry_ciudad.grid(row=1, column=1,pady=(20, 0))

        # Botones
        self.btn_agregar = tk.Button(master, text="Agregar", command=self.agregar)
        self.btn_agregar.grid(row=1, column=0, columnspan=2, pady=(100, 0), padx=(10, 0))

        # Lista para mostrar los registros
        self.lista = ttk.Treeview(master, columns=('ID', 'CC/NIT', 'Nombre', 'Dirección', 'Celular', 'Correo', 'Ciudad'), show='headings')
        self.lista.grid(row=0, rowspan=8, column=2, columnspan=5, pady=10, padx=(20,20))
        self.lista.heading('ID', text='ID')
        self.lista.heading('CC/NIT', text='CC/NIT')
        self.lista.heading('Nombre', text='Nombre')
        self.lista.heading('Dirección', text='Dirección')
        self.lista.heading('Celular', text='Celular')
        self.lista.heading('Correo', text='Correo')
        self.lista.heading('Ciudad', text='Ciudad')

        self.lista.column('ID', width=40)
        self.lista.column('CC/NIT', width=100)
        self.lista.column('Nombre', width=150)
        self.lista.column('Dirección', width=120)
        self.lista.column('Celular', width=80)
        self.lista.column('Correo', width=150)
        self.lista.column('Ciudad', width=100)

        # Ajuste de posición y margen de los botones
        self.btn_actualizar = tk.Button(master, text="Actualizar", command=self.abrir_editar_proveedor, bg="#CCFFFF")
        self.btn_actualizar.grid(row=9, column=5, pady=5, columnspan=2, padx=(0, 70), sticky='e')

        self.btn_eliminar = tk.Button(master, text="Eliminar", command=lambda: self.eliminar_proveedor(self.lista.selection()), bg="#FF9999")
        self.btn_eliminar.grid(row=9, column=5, pady=5, columnspan=2, padx=(0, 10), sticky='e')

        self.btn_cargar_datos = tk.Button(master, text="↻", command=self.cargar_datos_desde_db)
        self.btn_cargar_datos.grid(row=9, column=5, columnspan=2, pady=5, padx=(0, 140), sticky='e')

        self.btn_bulk_insert = tk.Button(master, text="Cargar productos XL", command=self.bulk_insert_desde_excel_proveedores)
        self.btn_bulk_insert.grid(row=9, column=0, pady=5, columnspan=2, padx=(50, 0), sticky='w')

        self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')

        # Cargar datos desde la base de datos
        self.cargar_datos_desde_db()

    def cargar_datos_desde_db(self):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL SELECT para obtener todos los proveedores
            cursor.execute("SELECT * FROM proveedores")

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
        cc_nit_val = self.cc_nit_var.get()
        nombre_val = self.nombre_var.get()
        direccion_val = self.direccion_var.get()
        celular_val = self.celular_var.get()
        correo_val = self.correo_var.get()
        ciudad_val = self.ciudad_var.get()

        # Validar que no haya campos vacíos
        if not cc_nit_val or not nombre_val or not direccion_val or not celular_val or not correo_val or not ciudad_val:
            tk.messagebox.showerror("Error", "Todos los campos deben ser completados.")
            return

        # Verificar si ya existe un proveedor con el mismo CC/NIT
        if self.existe_proveedor(cc_nit_val):
            tk.messagebox.showerror("Error", "Ya existe un proveedor con el mismo CC/NIT.")
            return

        # Agregar el nuevo registro a la lista
        self.lista.insert('', 'end',
                          values=(cc_nit_val, nombre_val, direccion_val, celular_val, correo_val, ciudad_val))

        # Insertar en la base de datos
        self.insertar_proveedor_en_db(cc_nit_val, nombre_val, direccion_val, celular_val, correo_val, ciudad_val)

        # Limpiar los campos de entrada después de agregar
        self.limpiar_campos()

    def existe_proveedor(self, cc_nit):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL SELECT para verificar si ya existe un proveedor con el mismo CC/NIT
            cursor.execute("SELECT * FROM proveedores WHERE cc_nit = ?", (cc_nit,))

            # Obtener el primer registro (si existe)
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro is not None

        except sqlite3.Error as e:
            print(f"Error al verificar si existe el proveedor en la base de datos: {e}")
            return False

    def abrir_editar_proveedor(self):
        # Obtener el índice seleccionado en la lista
        seleccion = self.lista.selection()
        if not seleccion:
            tk.messagebox.showinfo("Información", "Por favor, seleccione un proveedor.")
            return

        # Obtener los valores del proveedor seleccionado
        id_proveedor_seleccionado = self.lista.item(seleccion, 'values')[0]
        cc_nit_val = self.lista.item(seleccion, 'values')[1]
        nombre_val = self.lista.item(seleccion, 'values')[2]
        direccion_val = self.lista.item(seleccion, 'values')[3]
        celular_val = self.lista.item(seleccion, 'values')[4]
        correo_val = self.lista.item(seleccion, 'values')[5]
        # Asegurarse de que haya al menos 7 elementos antes de intentar acceder al índice 6
        ciudad_val = self.lista.item(seleccion, 'values')[6] if len(self.lista.item(seleccion, 'values')) > 6 else ''

        # Crear una nueva ventana emergente (Toplevel)
        ventana_edicion = tk.Toplevel(self)

        # Crear una instancia de FormularioEnvio en la nueva ventana
        formulario_envio = FormularioEnvio(ventana_edicion)
        formulario_envio.id_var.set(id_proveedor_seleccionado)
        formulario_envio.cc_nit_var.set(cc_nit_val)
        formulario_envio.nombre_var.set(nombre_val)
        formulario_envio.direccion_var.set(direccion_val)
        formulario_envio.celular_var.set(celular_val)
        formulario_envio.correo_var.set(correo_val)
        formulario_envio.ciudad_var.set(ciudad_val)

        # Mostrar la ventana de edición
        formulario_envio.mostrar_ventana()

    def bulk_insert_desde_excel_proveedores(self):
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
            for row_number, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                # Tomar los valores de las columnas relevantes (ajusta según tus necesidades)
                cc_nit, nombre, direccion, celular, correo, ciudad = row[:6]

                # Establecer valores predeterminados si la dirección o el correo están vacíos
                direccion = direccion or ciudad  # Establecer ciudad como dirección predeterminada
                correo = correo or "NoTiene"

                # Asegurarse de que hay al menos 6 valores en la fila
                if len(row) >= 6:
                    # Llamar a la función para insertar en la base de datos
                    self.insertar_proveedor_en_db(cc_nit, nombre, direccion, celular, correo, ciudad)

                else:
                    print(
                        f"Error: Se esperaban al menos 6 valores, pero se encontraron {len(row)} valores en la fila {row_number}.")
                    print(f"Valores en la fila {row_number}: {row[:6]}")

            # Cerrar el archivo Excel después de leer
            workbook.close()

            # Actualizar cualquier otra cosa necesaria después de realizar el bulk insert
            # ...

        except Exception as e:
            print(f"Error al procesar el archivo Excel: {e}")

    def insertar_proveedor_en_db(self, cc_nit, nombre, direccion, celular, correo, ciudad):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL INSERT
            cursor.execute(
                "INSERT INTO proveedores (cc_nit, nombre, direccion, celular, correo, ciudad) VALUES (?, ?, ?, ?, ?, ?)",
                (cc_nit, nombre, direccion, celular, correo, ciudad))

            # Confirmar la transacción
            self.conexion.commit()

            # Cerrar el cursor
            cursor.close()

        except sqlite3.Error as e:
            print(f"Error al insertar proveedor en la base de datos: {e}")

    def actualizar(self):
        # Obtener el índice seleccionado en la lista
        seleccion = self.lista.selection()
        if seleccion:
            # Obtener el ID del proveedor seleccionado
            id_proveedor_seleccionado = self.lista.item(seleccion, 'values')[0]

            # Obtener los nuevos valores de las variables de control
            cc_nit_val = self.cc_nit_var.get()
            nombre_val = self.nombre_var.get()
            direccion_val = self.direccion_var.get()
            celular_val = self.celular_var.get()
            correo_val = self.correo_var.get()
            ciudad_val = self.ciudad_var.get()

            # Actualizar el registro en la lista
            self.lista.item(seleccion, values=(
                id_proveedor_seleccionado, cc_nit_val, nombre_val, direccion_val, celular_val, correo_val, ciudad_val))

            # Actualizar en la base de datos
            self.actualizar_proveedor_en_db(id_proveedor_seleccionado, cc_nit_val, nombre_val, direccion_val,
                                            celular_val,
                                            correo_val, ciudad_val)

            # Limpiar los campos de entrada después de actualizar
            self.limpiar_campos()

    def actualizar_proveedor_desde_edicion(self, ventana_edicion):
        # Obtener los nuevos valores de las variables de la ventana de edición
        id_proveedor_val = ventana_edicion.id_var.get()
        cc_nit_val = ventana_edicion.cc_nit_var.get()
        nombre_val = ventana_edicion.nombre_var.get()
        direccion_val = ventana_edicion.direccion_var.get()
        celular_val = ventana_edicion.celular_var.get()
        correo_val = ventana_edicion.correo_var.get()
        ciudad_val = ventana_edicion.ciudad_var.get()

        # Comprobaciones antes de actualizar
        if not id_proveedor_val or not cc_nit_val or not nombre_val:
            tk.messagebox.showerror("Error", "ID Proveedor, CC/NIT y Nombre son campos obligatorios.")
            return

        try:
            # Actualizar el registro en la lista
            self.lista.item(self.lista.selection(), values=(
                id_proveedor_val, cc_nit_val, nombre_val, direccion_val, celular_val, correo_val, ciudad_val))

            # Actualizar en la base de datos
            self.actualizar_proveedor_en_db(id_proveedor_val, cc_nit_val, nombre_val, direccion_val, celular_val,
                                            correo_val, ciudad_val)

            # Limpiar los campos de entrada después de actualizar
            ventana_edicion.limpiar_campos()
            ventana_edicion.destroy()

        except Exception as e:
            print(f"Error al actualizar proveedor desde la ventana de edición: {e}")
            tk.messagebox.showerror("Error",
                                    "Error al actualizar proveedor. Consulta la consola para obtener más detalles.")

    def actualizar_proveedor_en_db(self, id_proveedor, cc_nit, nombre, direccion, celular, correo, ciudad):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL UPDATE
            cursor.execute(
                "UPDATE proveedores SET cc_nit=?, nombre=?, direccion=?, celular=?, correo=?, ciudad=? WHERE id_proveedor=?",
                (cc_nit, nombre, direccion, celular, correo, ciudad, id_proveedor))

            # Confirmar la transacción
            self.conexion.commit()

            # Cerrar el cursor
            cursor.close()

        except sqlite3.Error as e:
            print(f"Error al actualizar proveedor en la base de datos: {e}")

    def eliminar_proveedor(self, item):
        id_proveedor_seleccionado = self.lista.item(item, 'values')[
            0]  # Obtener el valor de id_proveedor del registro seleccionado
        if id_proveedor_seleccionado:
            confirmar_eliminar = tk.messagebox.askyesno("Eliminar Registro",
                                                        f"¿Estás seguro de eliminar el registro con ID Proveedor {id_proveedor_seleccionado}?")
            if confirmar_eliminar:
                # Lógica para eliminar el registro de la base de datos
                try:
                    # Crear un cursor
                    cursor = self.conexion.cursor()

                    # Ejecutar la sentencia SQL DELETE
                    cursor.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor_seleccionado,))

                    # Confirmar la transacción
                    self.conexion.commit()

                    # Cerrar el cursor
                    cursor.close()

                    # Eliminar el registro de la lista
                    self.lista.delete(item)

                    # Limpiar los campos de entrada después de eliminar
                    self.limpiar_campos()

                except sqlite3.Error as e:
                    print(f"Error al eliminar proveedor de la base de datos: {e}")

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.cc_nit_var.set('')
        self.nombre_var.set('')
        self.direccion_var.set('')
        self.celular_var.set('')
        self.correo_var.set('')
        self.ciudad_var.set('')

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
# Aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ProveedorCRUD(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')  # Conectar a la base de datos
    app.grid(row=0, column=0, sticky="nsew")
    root.protocol("WM_DELETE_WINDOW", app.cerrar_conexion)  # Vincular al evento de cierre
    root.geometry("960x315")
    root.mainloop()
