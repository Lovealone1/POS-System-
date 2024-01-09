import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class VistaGestionSaldo(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Gestión de Saldo")

        # Etiqueta y ComboBox para seleccionar el banco
        self.label_banco = tk.Label(self, text="Banco:")
        self.label_banco.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.bancos = self.obtener_lista_bancos()
        self.selected_banco = tk.StringVar(self)
        self.dropdown_banco = ttk.Combobox(self, textvariable=self.selected_banco, values=self.bancos, state="readonly")
        self.dropdown_banco.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Etiqueta y Campo de entrada para el saldo
        self.label_saldo = tk.Label(self, text="Saldo:")
        self.label_saldo.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.entry_saldo = tk.Entry(self, width=23)
        self.entry_saldo.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Botones para agregar y quitar saldo
        self.boton_quitar_saldo = tk.Button(self, text="Quitar Saldo", command=self.quitar_saldo, bg="lightcoral")
        self.boton_quitar_saldo.grid(row=2, column=1, pady=10, padx=(100, 10))

        self.boton_agregar_saldo = tk.Button(self, text="Agregar Saldo", command=self.agregar_saldo, bg="lightgreen")
        self.boton_agregar_saldo.grid(row=2, column=1, pady=10, padx=(0, 100))

        # Etiqueta para mostrar el saldo actual
        self.label_saldo_actual = tk.Label(self, text="Saldo Actual: $0.00")
        self.label_saldo_actual.grid(row=3, column=0, columnspan=2, pady=10)
        self.dropdown_banco.bind("<<ComboboxSelected>>", self.actualizar_saldo_label)

    def obtener_lista_bancos(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener la lista de nombres de bancos
            cursor.execute("SELECT nombre_banco FROM bancos")
            bancos = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Retornar la lista de nombres de bancos
            return [nombre_banco[0] for nombre_banco in bancos]

        except sqlite3.Error as e:
            print(f"Error al obtener la lista de bancos: {e}")
            return []

    def quitar_saldo(self):
        # Método para actualizar el saldo del banco
        nombre_banco_seleccionado = self.selected_banco.get()
        monto = self.obtener_monto_ingresado()

        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Obtener el saldo actual del banco
            cursor.execute("SELECT saldo FROM bancos WHERE nombre_banco = ?", (nombre_banco_seleccionado,))
            saldo_actual = cursor.fetchone()[0]

            # Actualizar el saldo del banco (restar el monto)
            nuevo_saldo = saldo_actual - monto
            cursor.execute("UPDATE bancos SET saldo = ? WHERE nombre_banco = ?",
                           (nuevo_saldo, nombre_banco_seleccionado))

            # Confirmar y cerrar la conexión
            conexion.commit()
            conexion.close()

            # Actualizar la etiqueta de saldo actual
            self.label_saldo_actual.config(text=f"Saldo Actual: ${nuevo_saldo:.2f}")
            messagebox.showinfo("Operación Exitosa", f"Saldo actualizado correctamente.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar el saldo: {e}")

    def obtener_monto_ingresado(self):
        try:
            monto = float(self.entry_saldo.get())
            return monto
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")
            return 0

    def agregar_saldo(self):
        # Método para actualizar el saldo del banco
        nombre_banco_seleccionado = self.selected_banco.get()
        monto = self.obtener_monto_ingresado()

        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Obtener el saldo actual del banco
            cursor.execute("SELECT saldo FROM bancos WHERE nombre_banco = ?", (nombre_banco_seleccionado,))
            saldo_actual = cursor.fetchone()[0]

            # Actualizar el saldo del banco
            nuevo_saldo = saldo_actual + monto
            cursor.execute("UPDATE bancos SET saldo = ? WHERE nombre_banco = ?", (nuevo_saldo, nombre_banco_seleccionado))

            # Confirmar y cerrar la conexión
            conexion.commit()
            conexion.close()

            # Actualizar la etiqueta de saldo actual
            self.label_saldo_actual.config(text=f"Saldo Actual: ${nuevo_saldo:.2f}")
            messagebox.showinfo("Operación Exitosa", f"Saldo actualizado correctamente.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar el saldo: {e}")

    def actualizar_saldo_label(self, event=None):
        # Método para actualizar el label del saldo actual al seleccionar un banco
        nombre_banco_seleccionado = self.selected_banco.get()

        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Obtener el saldo actual del banco
            cursor.execute("SELECT saldo FROM bancos WHERE nombre_banco = ?", (nombre_banco_seleccionado,))
            saldo_actual = cursor.fetchone()[0]

            # Actualizar la etiqueta de saldo actual
            self.label_saldo_actual.config(text=f"Saldo Actual: ${saldo_actual:.2f}")

            # Cerrar la conexión
            conexion.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el saldo: {e}")

# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    app = VistaGestionSaldo()
    app.mainloop()
