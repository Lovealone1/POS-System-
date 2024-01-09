import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry

class VistaEdicionGasto(tk.Toplevel):
    def __init__(self, master=None, gasto_id=None):
        super().__init__(master)
        self.master = master
        self.gasto_id = gasto_id
        self.title("Editar Gasto")

        # Variables de control
        self.tipo_gasto_var = tk.StringVar()
        self.monto_gasto_var = tk.DoubleVar()
        self.fecha_gasto_var = tk.StringVar()
        self.banco_var = tk.StringVar()

        # Crear etiquetas y campos de entrada
        tk.Label(self, text="Tipo de Gasto:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        ttk.Combobox(self, textvariable=self.tipo_gasto_var, values=self.obtener_tipos_gasto()).grid(row=0, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self, text="Monto de Gasto:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        ttk.Entry(self, textvariable=self.monto_gasto_var).grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self, text="Fecha de Gasto:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        DateEntry(self, textvariable=self.fecha_gasto_var, date_pattern='dd/mm/yyyy').grid(row=2, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self, text="Banco:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        ttk.Combobox(self, textvariable=self.banco_var, values=self.obtener_bancos()).grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Botones de acción
        ttk.Button(self, text="Guardar Cambios", command=self.guardar_cambios).grid(row=4, column=0, columnspan=2, pady=10)

        # Cargar datos del gasto seleccionado
        self.cargar_datos_gasto()

    def cargar_datos_gasto(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Obtener los datos del gasto seleccionado
            cursor.execute("SELECT tipo_gasto, monto_gasto, fecha_gasto, nombre_banco FROM gastos LEFT JOIN bancos ON gastos.id_banco = bancos.id WHERE id_gasto = ?", (self.gasto_id,))
            datos_gasto = cursor.fetchone()

            if datos_gasto:
                # Configurar los valores de las variables de control con los datos del gasto
                self.tipo_gasto_var.set(datos_gasto[0])
                self.monto_gasto_var.set(datos_gasto[1])
                self.fecha_gasto_var.set(datos_gasto[2])
                self.banco_var.set(datos_gasto[3])

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

        except sqlite3.Error as e:
            print(f"Error al cargar los datos del gasto: {e}")
            messagebox.showerror("Error", "Error al cargar los datos del gasto.")

    def obtener_tipos_gasto(self):
        # Método para obtener los tipos de gasto desde la base de datos
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT gasto FROM categorias_gastos")
            tipos_gasto = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conexion.close()

            return tipos_gasto
        except sqlite3.Error as e:
            print(f"Error al obtener tipos de gasto desde la base de datos: {e}")
            return []

    def obtener_bancos(self):
        # Método para obtener los bancos desde la base de datos
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre_banco FROM bancos")
            bancos = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conexion.close()

            return bancos
        except sqlite3.Error as e:
            print(f"Error al obtener bancos desde la base de datos: {e}")
            return []

    def guardar_cambios(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Obtener el id del banco seleccionado
            cursor.execute("SELECT id, saldo FROM bancos WHERE nombre_banco = ?", (self.banco_var.get(),))
            banco_info = cursor.fetchone()

            if not banco_info:
                messagebox.showwarning("Advertencia", "Banco no encontrado.")
                return

            id_banco, saldo_banco = banco_info

            # Obtener el monto_gasto actual
            cursor.execute("SELECT monto_gasto FROM gastos WHERE id_gasto = ?", (self.gasto_id,))
            monto_gasto_actual = cursor.fetchone()[0]

            # Obtener el nuevo monto_gasto
            nuevo_monto_gasto = self.monto_gasto_var.get()

            # Verificar si el monto_gasto actual es mayor al nuevo monto
            if monto_gasto_actual > nuevo_monto_gasto:
                # Restar la diferencia al saldo del banco
                diferencia = monto_gasto_actual - nuevo_monto_gasto
                nuevo_saldo = saldo_banco + diferencia
            elif monto_gasto_actual < nuevo_monto_gasto:
                # Sumar la diferencia al saldo del banco
                diferencia = nuevo_monto_gasto - monto_gasto_actual
                nuevo_saldo = saldo_banco - diferencia
            else:
                # Si el monto no cambia, no hay cambios en el saldo del banco
                nuevo_saldo = saldo_banco

            # Actualizar los datos del gasto en la base de datos
            cursor.execute(
                "UPDATE gastos SET tipo_gasto = ?, monto_gasto = ?, fecha_gasto = ?, id_banco = ? WHERE id_gasto = ?",
                (self.tipo_gasto_var.get(), nuevo_monto_gasto, self.fecha_gasto_var.get(), id_banco, self.gasto_id))

            # Actualizar el saldo en la tabla de bancos
            cursor.execute("UPDATE bancos SET saldo = ? WHERE id = ?", (nuevo_saldo, id_banco))

            # Confirmar la transacción
            conexion.commit()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Cerrar la ventana después de guardar los cambios
            self.destroy()

        except sqlite3.Error as e:
            print(f"Error al guardar los cambios en la base de datos: {e}")
            messagebox.showerror("Error", "Error al guardar los cambios en la base de datos.")

# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    root = tk.Tk()
    app = VistaEdicionGasto(master=root, gasto_id=1)  # Reemplaza 1 con el ID del gasto seleccionado
    root.mainloop()
