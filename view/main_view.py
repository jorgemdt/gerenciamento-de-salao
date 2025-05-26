import tkinter as tk
from tkinter import ttk, messagebox

class MainView:
    """
    Representa a janela Principal da aplicação, onde o CRUD é gerenciado.
    """
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        # Em vez de Toplevel, vamos configurar a janela principal (master)
        self.master.title("Gerenciamento de Agendamentos - Salão de Beleza")
        self.master.geometry("800x600+100+100")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Frames Principais ---
        # Frame para os formulários de entrada
        self.form_frame = ttk.LabelFrame(self.master, text="Dados do Agendamento", padding="10")
        self.form_frame.pack(pady=10, padx=10, fill=tk.X)

        # Frame para a lista (Treeview) e botões de ação
        self.list_frame = ttk.LabelFrame(self.master, text="Agendamentos", padding="10")
        self.list_frame.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # --- Widgets do Formulário (dentro de form_frame) ---
        self.labels = {}
        self.entries = {}
        fields = ["Nome", "Telefone", "Email", "Data (AAAA-MM-DD HH:MM)", "Valor (R$)", "Serviço"]
        
        # Usando grid para organizar o formulário
        for i, field in enumerate(fields):
            label_text = field.split('(')[0].strip() # Pega só o nome principal
            self.labels[label_text] = ttk.Label(self.form_frame, text=f"{field}:")
            self.labels[label_text].grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            
            self.entries[label_text] = ttk.Entry(self.form_frame, width=40)
            self.entries[label_text].grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

        # Frame para os botões do formulário
        self.form_button_frame = ttk.Frame(self.form_frame)
        self.form_button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

        self.add_button = ttk.Button(self.form_button_frame, text="Adicionar Novo")
        self.save_button = ttk.Button(self.form_button_frame, text="Salvar Alterações")
        self.clear_button = ttk.Button(self.form_button_frame, text="Limpar Campos")

        self.add_button.pack(side=tk.LEFT, padx=5)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        self.save_button.config(state=tk.DISABLED) # Desabilita 'Salvar' inicialmente

        # --- Widgets da Lista (dentro de list_frame) ---
        self.tree = ttk.Treeview(self.list_frame, 
                                 columns=("ID", "Nome", "Data", "Serviço", "Valor"), 
                                 show='headings')
                                 
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome Cliente")
        self.tree.heading("Data", text="Data/Hora")
        self.tree.heading("Serviço", text="Serviço")
        self.tree.heading("Valor", text="Valor (R$)")

        # Ajustando largura das colunas e ocultando ID
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("Data", width=120, anchor=tk.CENTER)
        self.tree.column("Serviço", width=150)
        self.tree.column("Valor", width=80, anchor=tk.E) # E = East (direita)

        # Adicionando Scrollbar
        self.scrollbar_y = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para os botões da lista
        self.list_button_frame = ttk.Frame(self.list_frame)
        self.list_button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.edit_button = ttk.Button(self.list_button_frame, text="Editar Selecionado")
        self.delete_button = ttk.Button(self.list_button_frame, text="Remover Selecionado")
        self.report_button = ttk.Button(self.list_button_frame, text="Gerar Relatório")

        self.edit_button.pack(pady=5, fill=tk.X)
        self.delete_button.pack(pady=5, fill=tk.X)
        self.report_button.pack(pady=15, fill=tk.X)
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)

        # --- Conectando ao Controller ---
        if self.controller:
            self.add_button.config(command=self.controller.handle_add_agendamento)
            self.save_button.config(command=self.controller.handle_update_agendamento)
            self.clear_button.config(command=self.clear_form) # Pode ser local ou via controller
            self.edit_button.config(command=self.controller.handle_edit_selection)
            self.delete_button.config(command=self.controller.handle_delete_agendamento)
            self.report_button.config(command=self.controller.handle_show_report)
            self.tree.bind("<<TreeviewSelect>>", self.controller.handle_tree_select)
            
    def populate_treeview(self, data):
        """Limpa e preenche a Treeview com os dados fornecidos."""
        # Limpa a árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Preenche com novos dados
        for row in data:
            # Seleciona apenas os campos que queremos exibir e na ordem correta
            # (id, nome, data, servico, valor)
            display_row = (row[0], row[1], row[4], row[6], f"{row[5]:.2f}") 
            self.tree.insert("", tk.END, values=display_row, iid=row[0]) # iid=row[0] usa o ID do banco como ID na tree

    def get_form_data(self):
        """Retorna os dados dos campos de entrada."""
        return {
            "Nome": self.entries["Nome"].get(),
            "Telefone": self.entries["Telefone"].get(),
            "Email": self.entries["Email"].get(),
            "Data": self.entries["Data"].get(),
            "Valor": self.entries["Valor"].get(),
            "Serviço": self.entries["Serviço"].get(),
        }

    def set_form_data(self, data):
        """Preenche os campos de entrada com os dados fornecidos."""
        self.clear_form() # Limpa antes de preencher
        self.entries["Nome"].insert(0, data.get("Nome", ""))
        self.entries["Telefone"].insert(0, data.get("Telefone", ""))
        self.entries["Email"].insert(0, data.get("Email", ""))
        self.entries["Data"].insert(0, data.get("Data", ""))
        self.entries["Valor"].insert(0, data.get("Valor", ""))
        self.entries["Serviço"].insert(0, data.get("Serviço", ""))

    def clear_form(self):
        """Limpa todos os campos de entrada."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection()) # Remove seleção da árvore
        self.save_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.add_button.config(state=tk.NORMAL)
        self.entries["Nome"].focus_set() # Foca no nome

    def get_selected_item_id(self):
        """Retorna o ID do item selecionado na Treeview."""
        try:
            selected_item = self.tree.selection()[0] # Pega o primeiro (e único) item selecionado
            # item_id = self.tree.item(selected_item, "values")[0] # Pega o valor da coluna 'ID'
            item_id = self.tree.item(selected_item)['values'][0] # Pega o ID que guardamos como iid
            return item_id
        except IndexError:
            return None # Nenhum item selecionado

    def enable_edit_delete_buttons(self, enable=True):
        """Habilita ou desabilita os botões Editar e Deletar."""
        state = tk.NORMAL if enable else tk.DISABLED
        self.edit_button.config(state=state)
        self.delete_button.config(state=state)
        
    def enable_save_button(self, enable=True):
        """Habilita ou desabilita o botão Salvar e desabilita Adicionar."""
        save_state = tk.NORMAL if enable else tk.DISABLED
        add_state = tk.DISABLED if enable else tk.NORMAL
        self.save_button.config(state=save_state)
        self.add_button.config(state=add_state)

    def show_message(self, title, message):
        """Exibe uma mensagem informativa."""
        messagebox.showinfo(title, message, parent=self.master)

    def show_error(self, title, message):
        """Exibe uma mensagem de erro."""
        messagebox.showerror(title, message, parent=self.master)

    def ask_question(self, title, message):
        """Faz uma pergunta (Sim/Não) e retorna True para Sim."""
        return messagebox.askyesno(title, message, parent=self.master)

    def show(self):
        """Mostra a janela principal."""
        self.master.deiconify() # Mostra a janela raiz

    def hide(self):
        """Esconde a janela principal."""
        self.master.withdraw()

    def on_closing(self):
        """Ação ao tentar fechar a janela principal."""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.master.destroy()

# Bloco Teste
if __name__ == '__main__':
    root = tk.Tk()

    class MockControllerForMain:
        def handle_add_agendamento(self): print("Clicou Adicionar")
        def handle_update_agendamento(self): print("Clicou Salvar")
        def handle_delete_agendamento(self): print("Clicou Remover")
        def handle_show_report(self): print("Clicou Relatório")
        def handle_tree_select(self, event): print("Item Selecionado")
        def handle_edit_selection(self): print("Clicou Editar")
        def load_data(self): # Simula carregar dados
            return [
                (1, "Ana Silva", "111", "ana@a.com", "2025-06-15 10:00", 50.00, "Corte"),
                (2, "Bruno Costa", "222", "bruno@b.com", "2025-06-15 11:30", 35.00, "Manicure"),
                (3, "Carla Dias", "333", "carla@c.com", "2025-06-16 14:00", 120.00, "Luzes"),
            ]

    mock_controller = MockControllerForMain()
    main_view = MainView(root, mock_controller)

    # Conecta os botões ao mock (necessário se controller=None no __init__)
    # Se passamos o mock, ele já tenta conectar. Aqui garantimos.
    main_view.add_button.config(command=mock_controller.handle_add_agendamento)
    main_view.save_button.config(command=mock_controller.handle_update_agendamento)
    main_view.delete_button.config(command=mock_controller.handle_delete_agendamento)
    main_view.report_button.config(command=mock_controller.handle_show_report)
    main_view.tree.bind("<<TreeviewSelect>>", mock_controller.handle_tree_select)
    main_view.edit_button.config(command=mock_controller.handle_edit_selection)

    # Popula com dados de teste
    test_data = mock_controller.load_data()
    main_view.populate_treeview(test_data)
    
    main_view.show() # Garante que a janela seja exibida
    root.mainloop()