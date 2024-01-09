import tkinter as tk
from tkinter import ttk
import sqlite3


class VistaDetallesPagoCredito(tk.Toplevel):
    def __init__(self, master=None, id_credito=None):
        super().__init__(master)
        self.title("Detalles de Pago")
        self.master = master
        self.id_credito = id_credito

        # Definir las columnas de la tabla, incluyendo la columna "Banco"
        self.tree = ttk.Treeview(self, columns=('ID Pago', 'Monto', 'Fecha de Pago', 'Banco'), show='headings')
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Configurar las columnas con su respectivo ancho y encabezado
        self.tree.column('ID Pago', width=80)
        self.tree.column('Monto', width=150)
        self.tree.column('Fecha de Pago', width=150)
        self.tree.column('Banco', width=150)

        self.tree.heading('ID Pago', text='ID Pago')
        self.tree.heading('Monto', text='Monto')
        self.tree.heading('Fecha de Pago', text='Fecha de Pago')
        self.tree.heading('Banco', text='Banco')  # Nuevo encabezado para la columna "Banco"

        self.scrollbar_y = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.cargar_detalles_pago_desde_db()



    def cargar_detalles_pago_desde_db(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener los detalles de los pagos
            cursor.execute("SELECT id, monto, fecha_pago, banco_id FROM pagos_creditos WHERE credito_id = ?",
                           (self.id_credito,))

            # Obtener los detalles de los pagos
            detalles_pago = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Agregar los detalles de los pagos a la lista
            for detalle in detalles_pago:
                id_pago = detalle[0]
                monto = detalle[1]
                fecha_pago = detalle[2]
                banco_id = detalle[3]

                # Obtener el nombre del banco
                nombre_banco = self.obtener_nombre_banco(banco_id)

                self.tree.insert('', 'end', values=(id_pago, monto, fecha_pago, nombre_banco))

        except sqlite3.Error as e:
            print(f"Error al cargar detalles de los pagos desde la base de datos: {e}")

    def obtener_nombre_banco(self, banco_id):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el nombre del banco
            cursor.execute("SELECT nombre_banco FROM bancos WHERE id = ?", (banco_id,))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Verificar si se encontró el nombre del banco
            if resultado is not None:
                nombre_banco = resultado[0]
                return nombre_banco
            else:
                return "Banco no encontrado"

        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del banco desde la base de datos: {e}")
            return "Error al obtener el nombre del banco"


        except sqlite3.Error as e:
            print(f"Error al cargar detalles de los pagos desde la base de datos: {e}")

    def obtener_nombre_credito(self, credito_id):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el nombre del crédito
            cursor.execute("SELECT nombre_credito FROM creditos WHERE id = ?", (credito_id,))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            # Verificar si se encontró el nombre del crédito
            if resultado is not None:
                nombre_credito = resultado[0]
                return nombre_credito
            else:
                return "Crédito no encontrado"

        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del crédito desde la base de datos: {e}")
            return "Error al obtener el nombre del crédito"

if __name__ == "__main__":
    # Supongamos que tienes el ID del crédito del cual deseas ver los detalles de los pagos
    id_credito_ejemplo = 1
    app = VistaDetallesPagoCredito(id_credito=id_credito_ejemplo)
    app.mainloop()
