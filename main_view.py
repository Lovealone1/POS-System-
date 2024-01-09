import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import calendar
from compras import CrudCompras
from ventas import VentaCRUD
from gastos import GastosApp
from panel_utilidades import VistaUtilidades
from ajuste_bancos import VistaGestionSaldo

class DashboardView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(bg="white")
        self.main_content = tk.Frame(self)  # Agregar este atributo
        self.main_content.grid(row=0, column=0, sticky="nsew")

        # Crear recuadro 1 (Efectivo)
        self.cargar_saldo_banco(row=1, column=0, text="Efectivo", banco_id=5, bg_color='#e6e6e6')

        # Crear recuadro 2 (Cuenta DGO)
        self.cargar_saldo_banco(row=1, column=1, text="Cuenta DGO", banco_id=2, bg_color='#e6e6e6')

        # Crear recuadro 3 (Cuenta AGL)
        self.cargar_saldo_banco(row=1, column=2, text="Cuenta AGL", banco_id=3, columnspan=2, bg_color='#e6e6e6')

        # Crear recuadro 4 (Nequi)
        self.cargar_saldo_banco(row=1, column=4, text="Nequi", banco_id=4, columnspan=2, bg_color='#e6e6e6')

        self.mostrar_grafico_ventas_por_mes()

        # Recuadro Ventas Totales
        self.cargar_ventas_totales(row=4, column=0, text="Ventas Totales", bg_color='#effce6')

        # Recuadro Utilidades Totales
        self.cargar_utilidades_totales(row=4, column=1, text="Utilidades Totales", bg_color='#effce6')

        # Recuadros adicionales en la parte inferior
        self.cargar_compras_credito(row=4, column=2, text="Compras Credito", columnspan=2, bg_color='#effce6')

        self.cargar_ventas_credito(row=4, column=4, text="Ventas Credito", columnspan=2, bg_color='#effce6')

        self.crear_botones(row=3, column=4)

        self.grid_columnconfigure(4, weight=1)

    def cargar_ventas_credito(self, row, column, text, columnspan=2, bg_color='#effce6'):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el saldo de ventas a crédito
            cursor.execute("SELECT saldo FROM ventas_credito WHERE id = 1")

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            if resultado is not None:
                # Si hay resultados, obtener el saldo de ventas a crédito
                saldo_ventas_credito = resultado[0]

                # Formatear el saldo de ventas a crédito como texto
                saldo_ventas_credito_text = f"${saldo_ventas_credito}"

                # Crear el recuadro con etiqueta
                self.crear_recuadro_con_etiqueta(row=row, column=column, text=text, value=saldo_ventas_credito_text,
                                                 columnspan=columnspan, bg_color=bg_color)
            else:
                # Si no hay resultados, imprimir un mensaje de error (puedes manejarlo de otra manera según tus necesidades)
                print("No se encontraron ventas a crédito registradas")

        except sqlite3.Error as e:
            print(f"Error al cargar el saldo de ventas a crédito desde la base de datos: {e}")

    def cargar_compras_credito(self, row, column, text, columnspan=2, bg_color='#effce6'):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el saldo de compras a crédito
            cursor.execute("SELECT saldo FROM compras_credito WHERE id = 1")

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            if resultado is not None:
                # Si hay resultados, obtener el saldo de compras a crédito
                saldo_compras_credito = resultado[0]

                # Formatear el saldo de compras a crédito como texto
                saldo_compras_credito_text = f"${saldo_compras_credito}"

                # Crear el recuadro con etiqueta
                self.crear_recuadro_con_etiqueta(row=row, column=column, text=text, value=saldo_compras_credito_text,
                                                 columnspan=columnspan, bg_color=bg_color)
            else:
                # Si no hay resultados, imprimir un mensaje de error (puedes manejarlo de otra manera según tus necesidades)
                print("No se encontraron compras a crédito registradas")

        except sqlite3.Error as e:
            print(f"Error al cargar el saldo de compras a crédito desde la base de datos: {e}")

    def cargar_utilidades_totales(self, row, column, text, columnspan=1, bg_color='white'):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el total de utilidades
            cursor.execute("SELECT SUM(utilidad) FROM utilidades")

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            if resultado is not None:
                # Si hay resultados, obtener el total de utilidades
                total_utilidades = resultado[0]

                # Formatear el total de utilidades como texto
                total_utilidades_text = f"${total_utilidades}"

                # Crear el recuadro con etiqueta
                self.crear_recuadro_con_etiqueta(row=row, column=column, text=text, value=total_utilidades_text,
                                                 columnspan=columnspan, bg_color=bg_color)
            else:
                # Si no hay resultados, imprimir un mensaje de error (puedes manejarlo de otra manera según tus necesidades)
                print("No se encontraron utilidades registradas")

        except sqlite3.Error as e:
            print(f"Error al cargar el total de utilidades desde la base de datos: {e}")

    def cargar_ventas_totales(self, row, column, text, columnspan=1, bg_color='white'):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para obtener el total de ventas
            cursor.execute("SELECT SUM(total) FROM ventas")

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            if resultado is not None:
                # Si hay resultados, obtener el total de ventas
                total_ventas = resultado[0]

                # Formatear el total de ventas como texto
                total_ventas_text = f"${total_ventas}"

                # Crear el recuadro con etiqueta
                self.crear_recuadro_con_etiqueta(row=row, column=column, text=text, value=total_ventas_text,
                                                 columnspan=columnspan, bg_color=bg_color)
            else:
                # Si no hay resultados, imprimir un mensaje de error (puedes manejarlo de otra manera según tus necesidades)
                print("No se encontraron ventas registradas")

        except sqlite3.Error as e:
            print(f"Error al cargar el total de ventas desde la base de datos: {e}")

    def cargar_saldo_banco(self, row, column, text, banco_id, columnspan=1, bg_color='white'):
        # Conectar a la base de datos
        conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para obtener el saldo del banco
        cursor.execute("SELECT saldo FROM bancos WHERE id = ?", (banco_id,))

        # Obtener el resultado de la consulta
        resultado = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

        if resultado is not None:
            # Si hay resultados, obtener el saldo del banco
            saldo = resultado[0]

            # Formatear el saldo como texto
            saldo_text = f"${saldo}"

            # Crear el recuadro con etiqueta
            self.crear_recuadro_con_etiqueta(row=row, column=column, text=text, value=saldo_text, columnspan=columnspan,
                                             bg_color=bg_color)
        else:
            # Si no hay resultados, imprimir un mensaje de error (puedes manejarlo de otra manera según tus necesidades)
            print(f"No se encontró un banco con id {banco_id}")

    def crear_recuadro_con_etiqueta(self, row, column, text, value, columnspan=1, bg_color='white'):
        frame = tk.Frame(self, borderwidth=2, relief="solid", width=200, height=100, bg=bg_color)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew", columnspan=columnspan)

        label_text = tk.Label(frame, text=text, font=("Arial", 12), anchor="center", bg=bg_color)
        label_text.grid(row=0, column=0, pady=2, sticky="ew")  # Ajuste de sticky para centrar horizontalmente

        label_value = tk.Label(frame, text=value, font=("Arial", 12), anchor="center", bg=bg_color)
        label_value.grid(row=1, column=0, pady=2, sticky="ew")

    def mostrar_grafico_ventas_por_mes(self):
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect('C:/Users/dgo34/Desktop/POS_System.db')
            cursor = conexion.cursor()

            # Consulta SQL para obtener las ventas por mes
            cursor.execute("""
                SELECT 
                    CASE substr(fecha_venta, 4, 2)
                        WHEN '01' THEN 'Ene'
                        WHEN '02' THEN 'Feb'
                        WHEN '03' THEN 'Mar'
                        WHEN '04' THEN 'Abr'
                        WHEN '05' THEN 'May'
                        WHEN '06' THEN 'Jun'
                        WHEN '07' THEN 'Jul'
                        WHEN '08' THEN 'Ago'
                        WHEN '09' THEN 'Sep'
                        WHEN '10' THEN 'Oct'
                        WHEN '11' THEN 'Nov'
                        WHEN '12' THEN 'Dic'
                        ELSE 'Desconocido'
                    END AS mes,
                    SUM(total) AS total_ventas
                FROM ventas
                WHERE substr(fecha_venta, 7, 4) = '2024'  -- Cambia '2022' al año deseado
                GROUP BY mes
                ORDER BY CAST(substr(fecha_venta, 4, 2) AS INTEGER);


            """)
            # Obtener los resultados de la consulta
            resultados = cursor.fetchall()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            if resultados:
                # Desempaquetar los resultados en listas separadas para meses y ventas
                meses, ventas_por_mes = zip(*resultados)

                # Mapear los números de mes a sus nombres respectivos
                nombres_meses = [calendar.month_name[int(mes)] if mes.isdigit() else mes for mes in meses]

                # Crear un gráfico de barras
                fig, ax = plt.subplots()
                ax.bar(nombres_meses, ventas_por_mes, color='blue')
                ax.set_ylabel('Ventas')
                ax.set_title('Ventas por Mes')

                # Mostrar el gráfico en la interfaz de usuario
                canvas = FigureCanvasTkAgg(fig, master=self)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=3, column=0, columnspan=4, pady=10, padx=40)
            else:
                print("No hay datos de ventas para mostrar.")

        except sqlite3.Error as e:
            print(f"Error al obtener datos de ventas desde la base de datos: {e}")

    def crear_botones(self, row, column):
        # Crear botones con bordes negros y color de fondo diferente
        button1 = tk.Button(self, text="Nueva Compra", command=self.on_button1_click, width=14, height=2, bd=1, highlightbackground="black", highlightthickness=1)
        button1.grid(row=row, column=column, pady=(0, 230), padx=(0, 80))

        button2 = tk.Button(self, text="Nueva Venta", command=self.on_button2_click, width=14, height=2, bd=1, highlightbackground="black", highlightthickness=1)
        button2.grid(row=row, column=column, pady=(0, 100), padx=(0, 80))

        button3 = tk.Button(self, text="Gastos", command=self.on_button3_click, width=14, height=2, bd=1, highlightbackground="black", highlightthickness=1)
        button3.grid(row=row, column=column, pady=(30, 0), padx=(0, 80))

        button4 = tk.Button(self, text="Utilidades", command=self.on_button4_click, width=14, height=2, bd=1, highlightbackground="black", highlightthickness=1)
        button4.grid(row=row, column=column, pady=(160, 0), padx=(0, 80))

    def on_button1_click(self):
        self.mostrar_vista(lambda: CrudCompras(self.main_content))

    def on_button2_click(self):
        self.mostrar_vista(lambda: VentaCRUD(self.main_content))

    def on_button3_click(self):
        self.mostrar_vista(lambda: GastosApp(self.main_content))

    def on_button4_click(self):
        self.mostrar_vista(lambda: VistaGestionSaldo(self.main_content))

    def mostrar_vista(self, vista_clase_factory):
        # Limpiar el contenido principal
        for child in self.main_content.winfo_children():
            child.destroy()

        # Crear y mostrar la nueva vista
        self.current_view = vista_clase_factory()

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardView(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.geometry("960x660")
    root.mainloop()
