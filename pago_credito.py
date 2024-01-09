import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class VistaPagoCredito(tk.Toplevel):
    def __init__(self, master=None, id_credito=None):
        super().__init__(master)
        self.master = master
        self.id_credito = id_credito
        self.title("Realizar Pago de Crédito")

        # Etiqueta (Label) para el monto
        self.label_monto = tk.Label(self, text="Monto:")
        self.label_monto.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        # Campo de entrada (Entry) para el monto
        self.entry_monto = tk.Entry(self)
        self.entry_monto.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Dropdown para los bancos
        self.label_banco = tk.Label(self, text="Banco:")
        self.label_banco.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        # Obtener la lista de bancos desde la base de datos
        self.bancos = self.obtener_lista_bancos()

        # Variable para el Dropdown
        self.selected_banco = tk.StringVar(self)
        self.dropdown_banco = ttk.Combobox(self, textvariable=self.selected_banco, values=self.bancos, state="readonly")
        self.dropdown_banco.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Botón de Pagar
        self.boton_pagar = tk.Button(self, text="Pagar", command=self.realizar_pago)
        self.boton_pagar.grid(row=2, column=0, columnspan=2, pady=10)

    def obtener_lista_bancos(self):
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_banco FROM bancos")
            bancos = cursor.fetchall()
            conexion.close()
            return [nombre_banco[0] for nombre_banco in bancos]
        except sqlite3.Error as e:
            print(f"Error al obtener la lista de bancos: {e}")
            return []

    def realizar_pago(self):
        monto_str = self.entry_monto.get()

        try:
            monto = float(monto_str)
            self.realizar_actualizacion(monto)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def realizar_actualizacion(self, monto):
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT saldo FROM creditos WHERE id = ?", (self.id_credito,))
            saldo_credito = cursor.fetchone()[0]

            nuevo_saldo_credito = saldo_credito - monto

            # Actualizar el saldo en la tabla de creditos
            cursor.execute("UPDATE creditos SET saldo = ? WHERE id = ?", (nuevo_saldo_credito, self.id_credito))

            # Insertar el pago en la tabla de pagos_creditos
            nombre_banco_seleccionado = self.selected_banco.get()
            cursor.execute("SELECT id FROM bancos WHERE nombre_banco = ?", (nombre_banco_seleccionado,))
            id_banco = cursor.fetchone()[0]

            cursor.execute("INSERT INTO pagos_creditos (credito_id, banco_id, monto) VALUES (?, ?, ?)",
                           (self.id_credito, id_banco, monto))

            # Actualizar el saldo en la tabla de bancos
            cursor.execute("UPDATE bancos SET saldo = saldo - ? WHERE id = ?", (monto, id_banco))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Pago Realizado",
                                f"Se ha realizado un pago de ${monto:.2f} para el crédito ID: {self.id_credito}")

        except sqlite3.Error as e:
            print(f"Error al realizar la actualización en la base de datos: {e}")


if __name__ == "__main__":
    # Reemplaza 'id_credito_ejemplo' con el ID del crédito que deseas pagar
    app = VistaPagoCredito(id_credito='id_credito_ejemplo')
    app.mainloop()
