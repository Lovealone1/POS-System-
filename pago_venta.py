import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importa el módulo de ttk para Dropdown
import sqlite3

class VistaPagoVenta(tk.Toplevel):
    def __init__(self, master=None, id_venta=None):
        super().__init__(master)
        self.master = master
        self.id_venta = id_venta
        self.title("Realizar Pago")

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
        # Conectar a la base de datos y obtener la lista de bancos
        try:
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_banco FROM bancos")
            bancos = cursor.fetchall()
            conexion.close()
            return [nombre_banco[0] for nombre_banco in bancos]  # Seleccionar el primer elemento de cada tupla
        except sqlite3.Error as e:
            print(f"Error al obtener la lista de bancos: {e}")
            return []

    def realizar_pago(self):
        # Método llamado al hacer clic en el botón "Pagar"
        monto_str = self.entry_monto.get()

        try:
            # Convertir el monto a un número
            monto = float(monto_str)

            # Lógica para realizar el pago (puedes personalizar esto según tus necesidades)
            self.realizar_actualizacion(monto)

            # Cierra la ventana después de realizar el pago
            self.destroy()

        except ValueError:
            # Si la conversión a número falla, muestra un mensaje de error
            messagebox.showerror("Error", "Ingrese un monto válido.")



    def realizar_actualizacion(self, monto):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Obtener el saldo restante actual en ventas
            cursor.execute("SELECT saldo_restante FROM ventas WHERE id = ?", (self.id_venta,))
            saldo_restante_venta = cursor.fetchone()[0]

            # Calcular el nuevo saldo restante en ventas
            nuevo_saldo_restante_venta = saldo_restante_venta - monto

            # Obtener el ID del banco seleccionado
            nombre_banco_seleccionado = self.selected_banco.get()
            cursor.execute("SELECT id FROM bancos WHERE nombre_banco = ?", (nombre_banco_seleccionado,))
            id_banco = cursor.fetchone()[0]

            # Actualizar el campo saldo_restante y forma_pago_id en la tabla ventas
            cursor.execute("UPDATE ventas SET saldo_restante = ?, forma_pago_id = ? WHERE id = ?",
                           (nuevo_saldo_restante_venta, id_banco, self.id_venta))

            # Verificar si el nuevo saldo restante en ventas es igual a 0
            if nuevo_saldo_restante_venta == 0:
                # Si es igual a 0, cambiar el estado de la venta a "Cancelada"
                cursor.execute("UPDATE ventas SET estado_venta = 'Cancelada' WHERE id = ?", (self.id_venta,))

            # Obtener el cliente asociado a la venta
            cursor.execute("SELECT cliente_id FROM ventas WHERE id = ?", (self.id_venta,))
            cliente_id = cursor.fetchone()[0]

            # Actualizar el saldo en la tabla de clientes
            cursor.execute("UPDATE clientes SET saldo = saldo - ? WHERE id_cliente = ?", (monto, cliente_id))

            # Actualizar la tabla de ventas_credito
            cursor.execute("UPDATE ventas_credito SET saldo = saldo - ? WHERE id = 1", (monto,))

            # Actualizar la tabla de bancos
            cursor.execute("UPDATE bancos SET saldo = saldo + ? WHERE id = ?", (monto, id_banco))

            # Confirmar y cerrar la conexión
            conexion.commit()
            conexion.close()

            # Mostrar un mensaje de éxito
            messagebox.showinfo("Pago Realizado",
                                f"Se ha realizado un pago de ${monto:.2f} para la venta ID: {self.id_venta}")

        except sqlite3.Error as e:
            print(f"Error al realizar la actualización en la base de datos: {e}")


# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    # Reemplaza 'id_venta_ejemplo' con el ID de la venta que deseas pagar
    app = VistaPagoVenta(id_venta='id_venta_ejemplo')
    app.mainloop()
