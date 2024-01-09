import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
from editar_gasto import VistaEdicionGasto

class GastosApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ventana de Gastos")
        # Variables de control
        self.tipo_gasto_var = tk.StringVar()
        self.monto_gasto_var = tk.DoubleVar()
        self.fecha_gasto_var = tk.StringVar()
        self.banco_var = tk.StringVar()

        frame_ingreso = ttk.Frame(self)
        frame_ingreso.grid(row=0, column=0, pady=10)

        # Crear el dropdown para el tipo de gasto
        tk.Label(frame_ingreso, text="Tipo de Gasto:").grid(row=0, column=0, padx=(0, 5))
        self.dropdown_tipo_gasto = ttk.Combobox(frame_ingreso, textvariable=self.tipo_gasto_var,
                                                values=self.obtener_tipos_gasto())
        self.dropdown_tipo_gasto.grid(row=0, column=1)

        # Crear el campo de entrada para el monto de gasto
        tk.Label(frame_ingreso, text="Monto de Gasto:").grid(row=0, column=2, padx=(10, 5))
        self.entry_monto_gasto = ttk.Entry(frame_ingreso, textvariable=self.monto_gasto_var)
        self.entry_monto_gasto.grid(row=0, column=3)

        # Crear el DatePicker para la fecha de gasto
        tk.Label(frame_ingreso, text="Fecha de Gasto:").grid(row=0, column=4, padx=(10, 5))
        self.date_picker = DateEntry(frame_ingreso, textvariable=self.fecha_gasto_var, date_pattern='dd/mm/yyyy')
        self.date_picker.grid(row=0, column=5)

        # Crear el dropdown para el banco
        tk.Label(frame_ingreso, text="Banco:").grid(row=0, column=6, padx=(10, 5))
        self.dropdown_banco = ttk.Combobox(frame_ingreso, textvariable=self.banco_var, values=self.obtener_bancos())
        self.dropdown_banco.grid(row=0, column=7)

        # Crear el botón de enviar
        ttk.Button(frame_ingreso, text="Enviar", command=self.registrar_gasto).grid(row=0, column=8, padx=(10, 0))

        # Crear la tabla para mostrar los registros
        self.tree_gastos = ttk.Treeview(self, columns=('ID Gasto', 'Tipo de Gasto', 'Monto', 'Fecha', 'Banco'),
                                        show='headings')
        self.tree_gastos.grid(row=1, column=0, pady=10, sticky="nsew", padx=(20,20))
        self.tree_gastos.heading('ID Gasto', text='ID Gasto')
        self.tree_gastos.heading('Tipo de Gasto', text='Tipo de Gasto')
        self.tree_gastos.heading('Monto', text='Monto')
        self.tree_gastos.heading('Fecha', text='Fecha')
        self.tree_gastos.heading('Banco', text='Banco')

        self.tree_gastos.column('ID Gasto', width=80)  # Establece el ancho de la columna 'ID Gasto' a 80
        self.tree_gastos.column('Tipo de Gasto', width=130)  # Establece el ancho de la columna 'Tipo de Gasto' a 150
        self.tree_gastos.column('Monto', width=80)  # Establece el ancho de la columna 'Monto' a 80
        self.tree_gastos.column('Fecha', width=100)  # Establece el ancho de la columna 'Fecha' a 120
        self.tree_gastos.column('Banco', width=100)

        # Botones de actualizar y eliminar
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=2, column=0, sticky="e", pady=(2, 5))

        ttk.Button(frame_botones, text="Actualizar", command=self.actualizar_gasto).grid(row=0, column=0, padx=5,
                                                                                         pady=2, sticky="e")
        ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_gasto).grid(row=0, column=1, padx=5,
                                                                                      pady=2, sticky="e")

        # Llamamos al método para cargar todos los gastos
        self.cargar_todos_gastos_desde_db()

    def obtener_tipos_gasto(self):
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT gasto FROM categorias_gastos")
            tipos_gasto = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conexion.close()

            return tipos_gasto
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener tipos de gasto desde la base de datos: {e}")
            return []

    def obtener_bancos(self):
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre_banco FROM bancos")
            bancos = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conexion.close()

            return bancos
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener bancos desde la base de datos: {e}")
            return []

    def registrar_gasto(self):
        tipo_gasto = self.tipo_gasto_var.get()
        monto_gasto = self.monto_gasto_var.get()
        fecha_gasto = self.fecha_gasto_var.get()
        banco = self.banco_var.get()

        # Validar que todos los campos estén llenos y tengan valores válidos
        if not tipo_gasto or not monto_gasto.isdigit() or float(monto_gasto) <= 0 or not fecha_gasto or not banco:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos correctamente.")
            return

        try:
            # Resto del código para registrar el gasto en la base de datos
            self.insertar_gasto_en_db(tipo_gasto, monto_gasto, fecha_gasto, banco)

            # Limpiar los campos después de un registro exitoso
            self.tipo_gasto_var.set('')
            self.monto_gasto_var.set('')
            self.fecha_gasto_var.set('')
            self.banco_var.set('')

            # Actualizar la visualización de los gastos
            self.cargar_todos_gastos_desde_db()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar el gasto en la base de datos: {e}")

    def cargar_todos_gastos_desde_db(self):
        try:
            for item in self.tree_gastos.get_children():
                self.tree_gastos.delete(item)

            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT id_gasto, tipo_gasto, monto_gasto, fecha_gasto, nombre_banco FROM gastos LEFT JOIN bancos ON gastos.id_banco = bancos.id")

            gastos = cursor.fetchall()

            cursor.close()
            conexion.close()

            for gasto in gastos:
                self.tree_gastos.insert('', 'end', values=gasto)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los gastos desde la base de datos: {e}")

    def insertar_gasto_en_db(self, tipo_gasto, monto_gasto, fecha_gasto, banco):
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT id, saldo FROM bancos WHERE nombre_banco = ?", (banco,))
            banco_info = cursor.fetchone()

            if banco_info:
                id_banco = banco_info[0]
            else:
                messagebox.showwarning("Advertencia", "Banco no encontrado.")
                return

            cursor.execute("INSERT INTO gastos (tipo_gasto, monto_gasto, fecha_gasto, id_banco) VALUES (?, ?, ?, ?)",
                           (tipo_gasto, monto_gasto, fecha_gasto, id_banco))

            nuevo_saldo = banco_info[1] - monto_gasto
            cursor.execute("UPDATE bancos SET saldo = ? WHERE id = ?", (nuevo_saldo, id_banco))

            conexion.commit()

            cursor.close()
            conexion.close()
        except sqlite3.Error as e:
            raise e

    def actualizar_gasto(self):
        selected_item = self.tree_gastos.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar.")
            return

        gasto_id = self.tree_gastos.item(selected_item, 'values')[0]

        ventana_edicion = VistaEdicionGasto(master=self.master, gasto_id=gasto_id)
        self.master.wait_window(ventana_edicion)
        self.cargar_todos_gastos_desde_db()

    def eliminar_gasto(self):
        selected_item = self.tree_gastos.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
            return

        gasto_id = self.tree_gastos.item(selected_item, 'values')[0]

        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este registro?")

        if not respuesta:
            return

        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT id_banco, monto_gasto FROM gastos WHERE id_gasto = ?", (gasto_id,))
            gasto_info = cursor.fetchone()

            if gasto_info:
                id_banco = gasto_info[0]
                monto_gasto = gasto_info[1]

                cursor.execute("DELETE FROM gastos WHERE id_gasto = ?", (gasto_id,))
                cursor.execute("UPDATE bancos SET saldo = saldo + ? WHERE id = ?", (monto_gasto, id_banco))

                conexion.commit()

                self.tipo_gasto_var.set('')
                self.monto_gasto_var.set('')
                self.fecha_gasto_var.set('')
                self.banco_var.set('')
                self.cargar_todos_gastos_desde_db()
            else:
                messagebox.showwarning("Advertencia", "No se encontró información del gasto.")

            cursor.close()
            conexion.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el gasto en la base de datos: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GastosApp(root)
    app.grid(row=0, column=0, sticky="nsew")  # Utiliza grid directamente en la instancia de tu aplicación
    root.mainloop()
