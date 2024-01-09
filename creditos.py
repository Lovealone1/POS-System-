import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
from pago_credito import VistaPagoCredito
from detalle_pago_credito import VistaDetallesPagoCredito
class CreditosApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Variables de control
        self.nombre_credito_var = tk.StringVar()
        self.monto_credito_var = tk.DoubleVar()
        self.fecha_creacion_var = tk.StringVar()

        frame_ingreso = ttk.Frame(self)
        frame_ingreso.grid(row=0, column=0, pady=10)

        # Crear el campo de entrada para el nombre del crédito
        tk.Label(frame_ingreso, text="Nombre del Crédito:").grid(row=0, column=0, padx=(0, 5))
        self.entry_nombre_credito = ttk.Entry(frame_ingreso, textvariable=self.nombre_credito_var)
        self.entry_nombre_credito.grid(row=0, column=1)

        # Crear el campo de entrada para el monto del crédito
        tk.Label(frame_ingreso, text="Monto del Crédito:").grid(row=0, column=2, padx=(10, 5))
        self.entry_monto_credito = ttk.Entry(frame_ingreso, textvariable=self.monto_credito_var)
        self.entry_monto_credito.grid(row=0, column=3)

        # Crear el DatePicker para la fecha de creación del crédito
        tk.Label(frame_ingreso, text="Fecha de Creación:").grid(row=0, column=4, padx=(10, 5))
        self.date_picker = DateEntry(frame_ingreso, textvariable=self.fecha_creacion_var, date_pattern='dd/mm/yyyy')
        self.date_picker.grid(row=0, column=5)

        # Crear el botón de enviar
        ttk.Button(frame_ingreso, text="Crear", command=self.registrar_credito).grid(row=0, column=6, padx=(10, 0))

        # Crear la tabla para mostrar los registros
        self.tree_creditos = ttk.Treeview(self, columns=('ID', 'Nombre del Crédito', 'Saldo', 'Fecha de Creación'),
                                          show='headings')
        self.tree_creditos.grid(row=1, column=0, pady=10, sticky="nsew", padx=(20, 20))
        self.tree_creditos.heading('ID', text='ID')
        self.tree_creditos.heading('Nombre del Crédito', text='Nombre del Crédito')
        self.tree_creditos.heading('Saldo', text='Saldo')
        self.tree_creditos.heading('Fecha de Creación', text='Fecha de Creación')

        self.tree_creditos.column('ID', width=80)  # Establece el ancho de la columna 'ID' a 80
        self.tree_creditos.column('Nombre del Crédito', width=200)  # Establece el ancho de la columna 'Nombre del Crédito' a 200
        self.tree_creditos.column('Saldo', width=80)  # Establece el ancho de la columna 'Saldo' a 80
        self.tree_creditos.column('Fecha de Creación', width=120)  # Establece el ancho de la columna 'Fecha de Creación' a 120

        # Botones de actualizar y eliminar
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=2, column=0, sticky="e", pady=(2, 5))

        ttk.Button(frame_botones, text="Realizar pago", command=self.actualizar_credito).grid(row=0, column=0, padx=5,
                                                                                           pady=2, sticky="e")
        ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_credito).grid(row=0, column=1, padx=5,
                                                                                        pady=2, sticky="e")
        ttk.Button(frame_botones, text="Ver detalles de pago", command=self.ver_detalles_pago).grid(row=0, column=0, padx=(0,575),
                                                                                              pady=2, sticky="e")

        # Llamamos al método para cargar todos los créditos
        self.cargar_todos_creditos_desde_db()

    def registrar_credito(self):
        nombre_credito = self.nombre_credito_var.get()
        monto_credito = self.monto_credito_var.get()
        fecha_creacion = self.fecha_creacion_var.get()

        # Validar que todos los campos estén llenos y tengan valores válidos
        if not nombre_credito or not self.es_numero_valido(monto_credito) or float(
                monto_credito) <= 0 or not fecha_creacion:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos correctamente.")
            return

        try:
            # Resto del código para registrar el crédito en la base de datos
            self.insertar_credito_en_db(nombre_credito, monto_credito, fecha_creacion)

            # Limpiar los campos después de un registro exitoso
            self.nombre_credito_var.set('')
            self.monto_credito_var.set('')
            self.fecha_creacion_var.set('')

            # Actualizar la visualización de los créditos
            self.cargar_todos_creditos_desde_db()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar el crédito en la base de datos: {e}")

    def es_numero_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def cargar_todos_creditos_desde_db(self):
        try:
            for item in self.tree_creditos.get_children():
                self.tree_creditos.delete(item)

            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT id, nombre_creditos, saldo, fecha_creacion FROM creditos")

            creditos = cursor.fetchall()

            cursor.close()
            conexion.close()

            for credito in creditos:
                self.tree_creditos.insert('', 'end', values=credito)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los créditos desde la base de datos: {e}")

    def insertar_credito_en_db(self, nombre_credito, monto_credito, fecha_creacion):
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("INSERT INTO creditos (nombre_creditos, saldo, fecha_creacion) VALUES (?, ?, ?)",
                           (nombre_credito, monto_credito, fecha_creacion))

            conexion.commit()

            cursor.close()
            conexion.close()
        except sqlite3.Error as e:
            raise e

    def actualizar_credito(self):
        selected_item = self.tree_creditos.selection()

        if selected_item:
            credito_id = self.tree_creditos.item(selected_item, 'values')[0]
            vista_pago = VistaPagoCredito(self.master, id_credito=credito_id)
        else:
            messagebox.showinfo("Error", "Selecciona una compra para realizar el pago.")

    def ver_detalles_pago(self):
        selected_item = self.tree_creditos.selection()

        if selected_item:
            credito_id = self.tree_creditos.item(selected_item, 'values')[0]
            vista_pago = VistaDetallesPagoCredito(self.master, id_credito=credito_id)
        else:
            messagebox.showinfo("Error", "Selecciona una compra para realizar el pago.")

    def eliminar_credito(self):
        selected_item = self.tree_creditos.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
            return

        credito_id = self.tree_creditos.item(selected_item, 'values')[0]

        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este registro?")

        if not respuesta:
            return

        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM creditos WHERE id = ?", (credito_id,))

            conexion.commit()

            cursor.close()
            conexion.close()

            # Actualizar la visualización de los créditos después de eliminar
            self.cargar_todos_creditos_desde_db()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el crédito en la base de datos: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CreditosApp(root)
    app.grid(row=0, column=0, sticky="nsew")  # Utiliza grid directamente en la instancia de tu aplicación
    root.mainloop()
