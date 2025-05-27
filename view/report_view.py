import tkinter as tk
from tkinter import ttk, messagebox

class ReportView:
    """
    Representa a janela de Relatórios da aplicação.
    Exibe uma lista de todos os agendamentos.
    """
    def __init__(self, master, controller):
        """
        Inicializa a ReportView.

        Args:
            master: A janela raiz (Tk) da aplicação.
            controller: O objeto AppController para comunicação (pode não ser
                        muito usado aqui, mas é bom ter para consistência).
        """
        self.master = master
        self.controller = controller

        # Cria uma Toplevel window para o relatório
        self.window = tk.Toplevel(self.master)
        self.window.title("Relatório de Agendamentos")
        self.window.geometry("900x500+150+150") # Um pouco maior para caber mais colunas
        self.window.resizable(True, True) # Permite redimensionar

        # Frame principal
        self.frame = ttk.Frame(self.window, padding="10")
        self.frame.pack(expand=True, fill=tk.BOTH)

        # --- Widgets ---
        # Treeview para exibir os dados
        self.tree = ttk.Treeview(self.frame,
                                 columns=("ID", "Nome", "Telefone", "Email", "Data", "Valor", "Serviço"),
                                 show='headings')

        # Definindo Cabeçalhos
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome Cliente")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Data", text="Data/Hora")
        self.tree.heading("Valor", text="Valor (R$)")
        self.tree.heading("Serviço", text="Serviço")

        # Definindo Largura das Colunas
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Nome", width=150)
        self.tree.column("Telefone", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Data", width=120, anchor=tk.CENTER)
        self.tree.column("Valor", width=80, anchor=tk.E)
        self.tree.column("Serviço", width=150)

        # Scrollbars (Vertical e Horizontal)
        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Layout com Scrollbars
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Botão Fechar
        self.close_button = ttk.Button(self.window, text="Fechar", command=self.destroy)
        self.close_button.pack(pady=10)

        # Define o que fazer ao fechar no 'X'
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

    def populate_report(self, data):
        """Limpa e preenche a Treeview com os dados do relatório."""
        # Limpa a árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Preenche com novos dados
        for row in data:
            # Garante que o valor seja formatado corretamente
            formatted_row = list(row)
            formatted_row[5] = f"{row[5]:.2f}"
            self.tree.insert("", tk.END, values=tuple(formatted_row))

    def show(self):
        """Mostra a janela de relatório."""
        self.window.deiconify()
        # Opcional: self.window.grab_set() se quiser que seja modal

    def destroy(self):
        """Destroi a janela de relatório."""
        self.window.destroy()


# Bloco Teste
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw() # Esconde a janela raiz

    # Dados de teste (simulando o que viria do Model)
    test_data = [
        (1, "Ana Silva", "111-1111", "ana@a.com", "2025-06-15 10:00", 50.00, "Corte"),
        (2, "Bruno Costa", "222-2222", "bruno@b.com", "2025-06-15 11:30", 35.00, "Manicure"),
        (3, "Carla Dias", "333-3333", "carla@c.com", "2025-06-16 14:00", 120.00, "Luzes"),
        (4, "Daniel Souza", "444-4444", "daniel@d.com", "2025-06-17 09:00", 40.00, "Barba"),
        (5, "Eliana Lima", "555-5555", "eliana@e.com", "2025-06-17 15:00", 70.00, "Pedicure e Manicure"),
        (6, "Fernando Reis", "666-6666", "fernando@f.com", "2025-06-18 16:00", 50.00, "Corte Masculino"),
    ] 

    # Instancia a ReportView (passando None para controller, pois não é usado no teste)
    report_view = ReportView(root, None)

    # Popula com os dados de teste
    report_view.populate_report(test_data)

    # Define o que fazer ao fechar a janela no modo de teste
    report_view.window.protocol("WM_DELETE_WINDOW", root.destroy)

    # Mostra a janela
    report_view.show()

    # Inicia o loop do Tkinter
    root.mainloop()
    print("Janela de relatório fechada.")