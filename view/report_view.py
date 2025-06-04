import tkinter as tk
from tkinter import ttk

class ReportView:
    """Representa a janela de Relatórios, exibindo agendamentos."""
    def __init__(self, master, controller):
        """Inicializa a ReportView com seus widgets."""
        self.master = master
        self.controller = controller

        self.window = tk.Toplevel(self.master)
        self.window.title("Relatório de Agendamentos")
        self.window.geometry("900x500+150+150")
        self.window.resizable(True, True)

        self.frame = ttk.Frame(self.window, padding="10")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(self.frame,
                                 columns=("ID", "Nome", "Telefone", "Email", "Data", "Valor", "Serviço"),
                                 show='headings')
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.heading("Nome", text="Nome Cliente"); self.tree.column("Nome", width=150)
        self.tree.heading("Telefone", text="Telefone"); self.tree.column("Telefone", width=100)
        self.tree.heading("Email", text="Email"); self.tree.column("Email", width=150)
        self.tree.heading("Data", text="Data/Hora"); self.tree.column("Data", width=120, anchor=tk.CENTER)
        self.tree.heading("Valor", text="Valor (R$)"); self.tree.column("Valor", width=80, anchor=tk.E)
        self.tree.heading("Serviço", text="Serviço"); self.tree.column("Serviço", width=150)

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.close_button = ttk.Button(self.window, text="Fechar", command=self.destroy)
        self.close_button.pack(pady=10)
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

    def populate_report(self, data):
        """Preenche o Treeview com os dados do relatório."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            formatted_row = list(row)
            formatted_row[5] = f"{row[5]:.2f}" # Formata valor
            self.tree.insert("", tk.END, values=tuple(formatted_row))

    def show(self):
        """Mostra a janela de relatório."""
        self.window.deiconify()

    def destroy(self):
        """Destroi a janela de relatório."""
        if self.window.winfo_exists():
            self.window.destroy()