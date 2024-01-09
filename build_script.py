import tkinter as tk
from tkinter import ttk
from dashboard import DashboardTopbar  # Asegúrate de importar tu vista principal

if __name__ == "__main__":
    root = tk.Tk()
    main_content = ttk.Frame(root)
    main_content.pack(side="top", fill="both", expand=True)
    app = DashboardTopbar(root)
    root.mainloop()