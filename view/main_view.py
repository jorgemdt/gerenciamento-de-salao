import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime # Precisaremos para conversão de data

class MainView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.master.title("Gerenciamento de Agendamentos - Salão de Beleza")
        self.master.geometry("800x600+100+100") # Ajuste conforme necessário
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- StringVars para campos com formatação especial ---
        self.data_var = tk.StringVar()
        self._data_var_trace_active = True # Flag para controle de recursão no trace

        # --- Registrando Comandos de Validação ---
        self.vcmd_digits = (self.master.register(self._validate_digits_only), '%P')
        self.vcmd_decimal = (self.master.register(self._validate_decimal_input), '%P')
        # Alterado: vcmd_date_action agora usa _validate_date_action e passa %d (action_code) e %S (text_being_inserted)
        self.vcmd_date_action = (self.master.register(self._validate_date_action), '%d', '%S')


        self.form_frame = ttk.LabelFrame(self.master, text="Dados do Agendamento", padding="10")
        self.form_frame.pack(pady=10, padx=10, fill=tk.X)

        self.list_frame = ttk.LabelFrame(self.master, text="Agendamentos", padding="10")
        self.list_frame.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        self._create_widgets()
        self.data_var.trace_add('write', self._format_date_trace)

    # --- Funções de Validação e Formatação ---
    def _validate_digits_only(self, P):
        return P == "" or P.isdigit()

    def _validate_decimal_input(self, P):
        if P == "": return True
        return all(char.isdigit() or char == '.' for char in P) and P.count('.') <= 1

    # Renomeada e modificada para usar action_code (%d)
    def _validate_date_action(self, action_code, text_being_inserted):
        """
        Valida a ação no campo de data.
        action_code: '0' para delete, '1' para insert, '-1' para outros.
        text_being_inserted: O texto sendo inserido (para action_code '1').
        """
        if action_code == '0':  # Ação de Deletar (Backspace, Delete)
            return True         # Sempre permite a deleção, o trace fará a reformatação

        if action_code == '1':  # Ação de Inserir
            # Permite apenas que dígitos sejam inseridos diretamente pelo usuário
            if not text_being_inserted.isdigit():
                # self.master.bell() # Opcional: Som de erro se caractere não for dígito
                return False

            # Verifica se a inserção do(s) dígito(s) excederia 8 dígitos no total
            # self.data_var.get() contém o texto ANTES da inserção atual
            current_digits_in_var = "".join(filter(str.isdigit, self.data_var.get()))
            num_new_digits = len("".join(filter(str.isdigit, text_being_inserted)))

            if len(current_digits_in_var) + num_new_digits > 8:
                # self.master.bell() # Opcional: Som de erro se exceder limite
                return False # Excedeu o limite de 8 dígitos
            return True # Permite a inserção do dígito
        
        return True # Permite outras ações (foco, etc.) que não sejam insert ou delete

    def _format_date_trace(self, var_name, index, mode):
        if not self._data_var_trace_active:
            return

        self._data_var_trace_active = False # Previne recursão

        current_text = self.data_var.get() # Texto após a ação permitida pelo validatecommand
        original_digits = "".join(filter(str.isdigit, current_text))
        
        formatted_text = ""
        if len(original_digits) > 0:
            formatted_text = original_digits[0:2] # DD
        if len(original_digits) > 2: # Adiciona '/' apenas se houver dígitos para 'mm'
            formatted_text += "/" + original_digits[2:4] # MM
        if len(original_digits) > 4: # Adiciona '/' apenas se houver dígitos para 'aaaa'
            formatted_text += "/" + original_digits[4:8] # AAAA (até 8 dígitos no total)

        self.data_var.set(formatted_text)
        
        if self.entries.get("Data"): 
            self.entries["Data"].icursor(tk.END)

        self._data_var_trace_active = True

    def _create_widgets(self):
        self.labels = {}
        self.entries = {}
        fields = ["Nome", "Telefone", "Email", "Data (DD/MM/AAAA)", "Valor (R$)", "Serviço"]
        
        for i, field in enumerate(fields):
            label_text = field.split('(')[0].strip()
            self.labels[label_text] = ttk.Label(self.form_frame, text=f"{field}:")
            self.labels[label_text].grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            
            if label_text == "Data":
                self.entries[label_text] = ttk.Entry(self.form_frame, width=40, 
                                                     textvariable=self.data_var,
                                                     validate='key', 
                                                     validatecommand=self.vcmd_date_action) # Alterado para vcmd_date_action
            else:
                self.entries[label_text] = ttk.Entry(self.form_frame, width=40)

            self.entries[label_text].grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

            if label_text == "Telefone":
                self.entries[label_text].config(validate='key', validatecommand=self.vcmd_digits)
            elif label_text == "Valor":
                self.entries[label_text].config(validate='key', validatecommand=self.vcmd_decimal)
        
        self.form_button_frame = ttk.Frame(self.form_frame)
        self.form_button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

        self.add_button = ttk.Button(self.form_button_frame, text="Adicionar Novo", command=self._handle_add_click)
        self.save_button = ttk.Button(self.form_button_frame, text="Salvar Alterações", command=self._handle_save_click)
        self.clear_button = ttk.Button(self.form_button_frame, text="Limpar Campos", command=self._handle_clear_click)

        self.add_button.pack(side=tk.LEFT, padx=5)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        self.save_button.config(state=tk.DISABLED)

        self.tree = ttk.Treeview(self.list_frame, 
                                 columns=("ID", "Nome", "Data", "Serviço", "Valor"), 
                                 show='headings')
                                 
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome Cliente")
        self.tree.heading("Data", text="Data/Hora") 
        self.tree.heading("Serviço", text="Serviço")
        self.tree.heading("Valor", text="Valor (R$)")

        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("Data", width=120, anchor=tk.CENTER)
        self.tree.column("Serviço", width=150)
        self.tree.column("Valor", width=80, anchor=tk.E)

        self.scrollbar_y = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_button_frame = ttk.Frame(self.list_frame)
        self.list_button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.edit_button = ttk.Button(self.list_button_frame, text="Editar Selecionado", command=self._handle_edit_click)
        self.delete_button = ttk.Button(self.list_button_frame, text="Remover Selecionado", command=self._handle_delete_click)
        self.report_button = ttk.Button(self.list_button_frame, text="Gerar Relatório", command=self._handle_report_click)

        self.edit_button.pack(pady=5, fill=tk.X)
        self.delete_button.pack(pady=5, fill=tk.X)
        self.report_button.pack(pady=15, fill=tk.X)
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)

        self.tree.bind("<<TreeviewSelect>>", self._handle_tree_select_event)

    def _handle_add_click(self):
        if self.controller: self.controller.handle_add_agendamento()
    
    def _handle_save_click(self):
        if self.controller: self.controller.handle_update_agendamento()

    def _handle_clear_click(self):
        self.clear_form() 
        if self.controller: self.controller.handle_clear_form_request()

    def _handle_edit_click(self):
        if self.controller: self.controller.handle_edit_selection()

    def _handle_delete_click(self):
        if self.controller: self.controller.handle_delete_agendamento()

    def _handle_report_click(self):
        if self.controller: self.controller.handle_show_report()

    def _handle_tree_select_event(self, event):
        if self.controller: self.controller.handle_tree_select(event)

    def populate_treeview(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            db_date_str = row[4] 
            display_date_tree = db_date_str 
            try:
                dt_obj = datetime.strptime(db_date_str.split(" ")[0], "%Y-%m-%d")
                display_date_tree = dt_obj.strftime("%d/%m/%Y") 
            except ValueError:
                pass 

            display_row = (row[0], row[1], display_date_tree, row[6], f"{row[5]:.2f}") 
            self.tree.insert("", tk.END, values=display_row, iid=row[0])

    def get_form_data(self):
        return {
            "Nome": self.entries["Nome"].get(),
            "Telefone": self.entries["Telefone"].get(),
            "Email": self.entries["Email"].get(),
            "Data": self.data_var.get(), 
            "Valor": self.entries["Valor"].get(),
            "Serviço": self.entries["Serviço"].get(),
        }

    def set_form_data(self, data_dict_from_controller): 
        self.clear_form_fields()
        self.entries["Nome"].insert(0, data_dict_from_controller.get("Nome", ""))
        self.entries["Telefone"].insert(0, data_dict_from_controller.get("Telefone", ""))
        self.entries["Email"].insert(0, data_dict_from_controller.get("Email", ""))
        
        db_date_str = data_dict_from_controller.get("Data", "")
        display_date_form = ""
        if db_date_str:
            try:
                dt_obj = datetime.strptime(db_date_str.split(" ")[0], "%Y-%m-%d")
                display_date_form = dt_obj.strftime("%d/%m/%Y")
            except ValueError:
                display_date_form = "Data Inválida" 
        self.data_var.set(display_date_form) 

        self.entries["Valor"].insert(0, data_dict_from_controller.get("Valor", ""))
        self.entries["Serviço"].insert(0, data_dict_from_controller.get("Serviço", ""))

    def clear_form_fields(self):
        for key, entry in self.entries.items():
            if key == "Data":
                self.data_var.set("") 
            else:
                entry.delete(0, tk.END)
        if self.entries.get("Nome"): 
            self.entries["Nome"].focus_set()

    def clear_form(self):
        self.clear_form_fields()
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])
        self.save_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.add_button.config(state=tk.NORMAL)
        
    def get_selected_item_id(self):
        try:
            selected_item = self.tree.selection()[0]
            item_id = self.tree.item(selected_item)['values'][0]
            return item_id
        except IndexError:
            return None

    def enable_edit_delete_buttons(self, enable=True):
        state = tk.NORMAL if enable else tk.DISABLED
        self.edit_button.config(state=state)
        self.delete_button.config(state=state)
        
    def enable_save_button(self, enable=True):
        save_state = tk.NORMAL if enable else tk.DISABLED
        add_state = tk.DISABLED if enable else tk.NORMAL
        self.save_button.config(state=save_state)
        self.add_button.config(state=add_state)

    def show_message(self, title, message):
        messagebox.showinfo(title, message, parent=self.master)

    def show_error(self, title, message):
        messagebox.showerror(title, message, parent=self.master)

    def ask_question(self, title, message):
        return messagebox.askyesno(title, message, parent=self.master)

    def show(self):
        self.master.deiconify()

    def hide(self):
        self.master.withdraw()

    def on_closing(self):
        if self.controller:
            if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
                self.master.destroy()
        else: 
            if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
                self.master.destroy()

