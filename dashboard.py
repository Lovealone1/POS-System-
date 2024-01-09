import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from cliente import CrudApp
from proveedor import ProveedorCRUD
from producto import ProductoCRUD
from visualizar_compras import VistaCompras
from visualizar_ventas import VistaVentas
from gastos import GastosApp
from main_view import DashboardView
from panel_utilidades import VistaUtilidades
from creditos import CreditosApp
class DashboardTopbar:
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard")

        # Configurar el tema

        # Barra superior (topbar)
        self.topbar = ttk.Frame(master, height=80)
        self.topbar.pack(side="top", fill="x", padx=10, pady=(15, 15))

        # Contenido principal
        self.main_content = ttk.Frame(master, relief="raised")
        self.main_content.pack(side="top", fill="both", expand=True)
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Botones en la barra superior con más margen y estilo plano
        self.btn_return = ttk.Button(self.topbar, text="←", command=self.return_view)
        self.btn_return.pack(side="left", padx=(0, 10))

        self.btn_cliente = ttk.Button(self.topbar, text="Clientes", command=self.abrir_crud_cliente)
        self.btn_cliente.pack(side="left", padx=(0, 10))

        self.btn_proveedor = ttk.Button(self.topbar, text="Proveedores", command=self.abrir_crud_proveedor)
        self.btn_proveedor.pack(side="left", padx=10)

        self.btn_producto = ttk.Button(self.topbar, text="Productos", command=self.abrir_crud_producto)
        self.btn_producto.pack(side="left", padx=10)

        self.btn_panel_compras = ttk.Button(self.topbar, text="Panel Compras", command=self.abrir_panel_compras)
        self.btn_panel_compras.pack(side="left", padx=10)

        self.btn_panel_ventas = ttk.Button(self.topbar, text="Panel Ventas", command=self.abrir_panel_ventas)
        self.btn_panel_ventas.pack(side="left", padx=10)

        self.btn_panel_utilidades = ttk.Button(self.topbar, text="Panel Utilidades", command=self.abrir_panel_utilidades)
        self.btn_panel_utilidades.pack(side="left", padx=10)

        self.btn_panel_creditos = ttk.Button(self.topbar, text="Creditos",
                                               command=self.abrir_panel_creditos)
        self.btn_panel_creditos.pack(side="left", padx=10)


        # Inicializar la vista actual como None
        self.current_view = None
        self.editar_cliente_window = None

        self.mostrar_vista(lambda: DashboardView(self.main_content))

    def abrir_crud_cliente(self):
        self.mostrar_vista(lambda: CrudApp(self.main_content))

    def abrir_crud_proveedor(self):
        self.mostrar_vista(lambda: ProveedorCRUD(self.main_content))

    def abrir_crud_producto(self):
        self.mostrar_vista(lambda: ProductoCRUD(self.main_content))

    def abrir_panel_compras(self):
        self.mostrar_vista(lambda: VistaCompras(self.main_content))

    def abrir_panel_ventas(self):
        self.mostrar_vista(lambda: VistaVentas(self.main_content))

    def return_view(self):
        self.mostrar_vista(lambda: DashboardView(self.main_content))

    def abrir_panel_utilidades(self):
        self.mostrar_vista(lambda: VistaUtilidades(self.main_content))

    def abrir_panel_creditos(self):
        self.mostrar_vista(lambda: CreditosApp(self.main_content))

    def mostrar_vista(self, vista_clase_factory):
        # Limpiar el contenido principal
        for child in self.main_content.winfo_children():
            child.destroy()

        # Crear y mostrar la nueva vista
        self.current_view = vista_clase_factory()
        self.current_view.grid(row=0, column=0, sticky="nsew")

# Aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    main_content = ttk.Frame(root)
    main_content.pack(side="top", fill="both", expand=True)
    app = DashboardTopbar(root)
    root.mainloop()
