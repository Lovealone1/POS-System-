import tkinter as tk
from tkinter import ttk
import sqlite3


class FormularioEnvio(ttk.Frame):
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
        self.label_referencia = ttk.Label(self, text="Referencia:")
        self.label_referencia.grid(row=0, column=0, sticky="e")
        self.entry_referencia = ttk.Entry(self, textvariable=self.referencia_var)
        self.entry_referencia.grid(row=0, column=1)

        self.label_descripcion = ttk.Label(self, text="Descripción:")
        self.label_descripcion.grid(row=1, column=0, sticky="e")
        self.entry_descripcion = ttk.Entry(self, textvariable=self.descripcion_var)
        self.entry_descripcion.grid(row=1, column=1)

        self.label_cantidad = ttk.Label(self, text="Cantidad:")
        self.label_cantidad.grid(row=2, column=0, sticky="e")
        self.entry_cantidad = ttk.Entry(self, textvariable=self.cantidad_var)
        self.entry_cantidad.grid(row=2, column=1)

        self.label_precio_compra = ttk.Label(self, text="Precio de Compra:")
        self.label_precio_compra.grid(row=3, column=0, sticky="e")
        self.entry_precio_compra = ttk.Entry(self, textvariable=self.precio_compra_var)
        self.entry_precio_compra.grid(row=3, column=1)

        self.label_precio_venta = ttk.Label(self, text="Precio de Venta:")
        self.label_precio_venta.grid(row=4, column=0, sticky="e")
        self.entry_precio_venta = ttk.Entry(self, textvariable=self.precio_venta_var,width=20)
        self.entry_precio_venta.grid(row=4, column=1)

        self.label_estado = ttk.Label(self, text="Estado:")
        self.label_estado.grid(row=5, column=0, sticky="e")
        self.estado_options = ["Activo", "Inactivo"]
        self.estado_dropdown = ttk.Combobox(self, textvariable=self.estado_var, values=self.estado_options, state="readonly", width=17)
        self.estado_dropdown.grid(row=5, column=1)

        # Botón de enviar
        self.btn_enviar = ttk.Button(self, text="Actualizar", command=self.enviar)
        self.btn_enviar.grid(row=6, column=0, columnspan=2, pady=10)

        self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
        self.master.protocol("WM_DELETE_WINDOW", self.enviar)

    def enviar(self):
        # Obtener los nuevos valores de las variables
        id_producto_val = self.id_var.get()
        referencia_val = self.referencia_var.get()
        descripcion_val = self.descripcion_var.get()
        cantidad_val = self.cantidad_var.get()
        precio_compra_val = self.precio_compra_var.get()
        precio_venta_val = self.precio_venta_var.get()
        estado_val = self.estado_var.get()

        # Actualizar producto en la base de datos
        self.actualizar_producto_en_db(id_producto_val, referencia_val, descripcion_val, cantidad_val, precio_compra_val,
                                       precio_venta_val, estado_val)

        # Limpiar los campos de entrada después de enviar
        self.limpiar_campos()
        # Cerrar la ventana
        self.master.destroy()

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

    def actualizar_producto_en_db(self, id_producto, referencia, descripcion, cantidad, precio_compra, precio_venta, estado):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL UPDATE
            cursor.execute(
                "UPDATE productos SET referencia=?, descripcion=?, cantidad=?, precio_compra=?, precio_venta=?, estado=? WHERE id=?",
                (referencia, descripcion, cantidad, precio_compra, precio_venta, estado, id_producto))

            # Confirmar la transacción
            self.conexion.commit()

            # Cerrar el cursor
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error al actualizar el producto en la base de datos: {e}")

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.referencia_var.set('')
        self.descripcion_var.set('')
        self.cantidad_var.set('')
        self.precio_compra_var.set('')
        self.precio_venta_var.set('')
        self.estado_var.set('')

    def mostrar_ventana(self):
        # Crear y mostrar la ventana de edición
        self.master.title("Editar Producto")
        self.pack()
        self.mainloop()

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioEnvio(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
    app.grid(row=0, column=0, sticky="nsew")
    app.grid(row=0, column=0, sticky="nsew")

    root.mainloop()
