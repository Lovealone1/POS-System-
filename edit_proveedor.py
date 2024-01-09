import tkinter as tk
from tkinter import ttk
import sqlite3


class FormularioEnvio(ttk.Frame):
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
        self.label_cc_nit = ttk.Label(self, text="CC/NIT:")
        self.label_cc_nit.grid(row=0, column=0, sticky="e")
        self.entry_cc_nit = ttk.Entry(self, textvariable=self.cc_nit_var)
        self.entry_cc_nit.grid(row=0, column=1)

        self.label_nombre = ttk.Label(self, text="Nombre:")
        self.label_nombre.grid(row=1, column=0, sticky="e")
        self.entry_nombre = ttk.Entry(self, textvariable=self.nombre_var)
        self.entry_nombre.grid(row=1, column=1)

        self.label_direccion = ttk.Label(self, text="Dirección:")
        self.label_direccion.grid(row=2, column=0, sticky="e")
        self.entry_direccion = ttk.Entry(self, textvariable=self.direccion_var)
        self.entry_direccion.grid(row=2, column=1)

        self.label_celular = ttk.Label(self, text="Celular:")
        self.label_celular.grid(row=3, column=0, sticky="e")
        self.entry_celular = ttk.Entry(self, textvariable=self.celular_var)
        self.entry_celular.grid(row=3, column=1)

        self.label_correo = ttk.Label(self, text="Correo:")
        self.label_correo.grid(row=4, column=0, sticky="e")
        self.entry_correo = ttk.Entry(self, textvariable=self.correo_var)
        self.entry_correo.grid(row=4, column=1)

        self.label_ciudad = ttk.Label(self, text="Ciudad:")
        self.label_ciudad.grid(row=5, column=0, sticky="e")
        self.entry_ciudad = ttk.Entry(self, textvariable=self.ciudad_var)
        self.entry_ciudad.grid(row=5, column=1)

        # Botón de enviar
        self.btn_enviar = ttk.Button(self, text="Actualizar", command=self.enviar)
        self.btn_enviar.grid(row=6, column=0, columnspan=2, pady=10)


        self.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')

    def enviar(self):
        # Obtener los nuevos valores de las variables
        id_cliente_val = self.id_var.get()
        cc_nit_val = self.cc_nit_var.get()
        nombre_val = self.nombre_var.get()
        direccion_val = self.direccion_var.get()
        celular_val = self.celular_var.get()
        correo_val = self.correo_var.get()
        ciudad_val = self.ciudad_var.get()

        # Actualizar cliente en la base de datos
        self.actualizar_cliente_en_db(id_cliente_val, cc_nit_val, nombre_val, direccion_val, celular_val, correo_val,
                                      ciudad_val)

        # Limpiar los campos de entrada después de enviar
        self.limpiar_campos()
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

    def actualizar_cliente_en_db(self, id_cliente, cc_nit, nombre, direccion, celular, correo, ciudad):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()

            # Ejecutar la sentencia SQL UPDATE
            cursor.execute(
                "UPDATE proveedores SET cc_nit=?, nombre=?, direccion=?, celular=?, correo=?, ciudad=? WHERE id_proveedor=?",
                (cc_nit, nombre, direccion, celular, correo, ciudad, id_cliente))

            # Confirmar la transacción
            self.conexion.commit()
            # Cerrar el cursor
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error al actualizar el cliente en la base de datos: {e}")

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.cc_nit_var.set('')
        self.nombre_var.set('')
        self.direccion_var.set('')
        self.celular_var.set('')
        self.correo_var.set('')
        self.ciudad_var.set('')

    def mostrar_ventana(self):
        # Crear y mostrar la ventana de edición
        self.master.title("Editar Proveedor")
        self.pack()
        self.mainloop()


# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioEnvio(root)
    app.conectar_base_datos('C:/Users/dgo34/Desktop/POS_System.db')
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
