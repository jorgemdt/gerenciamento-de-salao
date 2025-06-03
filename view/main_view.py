import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime # Precisaremos para conversão de data

class MainView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.master.title("Agendamentos - Salão de Beleza Neide Leila")
        self.master.geometry("800x650+100+100") # Aumentei um pouco a altura
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- StringVars para campos com formatação especial ---
        self.data_var = tk.StringVar()
        self.horario_var = tk.StringVar() # Nova StringVar para Horário
        self._data_var_trace_active = True
        self._horario_var_trace_active = True # Flag para Horário

        # --- Registrando Comandos de Validação ---
        self.vcmd_digits = (self.master.register(self._validate_digits_only), '%P')
        self.vcmd_decimal = (self.master.register(self._validate_decimal_input), '%P')
        self.vcmd_date_action = (self.master.register(self._validate_date_action), '%d', '%S')
        self.vcmd_time_action = (self.master.register(self._validate_time_action), '%d', '%S')


        self.form_frame = ttk.LabelFrame(self.master, text="Dados do Agendamento", padding="10")
        self.form_frame.pack(pady=10, padx=10, fill=tk.X)

        self.list_frame = ttk.LabelFrame(self.master, text="Agendamentos", padding="10")
        self.list_frame.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        self._create_widgets()
        # Adicionando traces
        self.data_var.trace_add('write', self._format_date_trace)
        self.horario_var.trace_add('write', self._format_time_trace) # Trace para Horário

    # --- Funções de Validação e Formatação ---
    def _validate_digits_only(self, P):
        return P == "" or P.isdigit()

    def _validate_decimal_input(self, P):
        if P == "": return True
        return all(char.isdigit() or char == '.' for char in P) and P.count('.') <= 1

    def _validate_date_action(self, action_code, text_being_inserted):
        if action_code == '0': return True
        if action_code == '1':
            if not text_being_inserted.isdigit(): return False
            current_digits_in_var = "".join(filter(str.isdigit, self.data_var.get()))
            num_new_digits = len("".join(filter(str.isdigit, text_being_inserted)))
            if len(current_digits_in_var) + num_new_digits > 8: return False
            return True
        return True

    def _format_date_trace(self, var_name, index, mode):
        if not self._data_var_trace_active: return
        self._data_var_trace_active = False
        
        current_text = self.data_var.get()
        original_digits = "".join(filter(str.isdigit, current_text))
        
        formatted_text = ""
        if len(original_digits) > 0: formatted_text = original_digits[0:2] # DD
        if len(original_digits) > 2: formatted_text += "/" + original_digits[2:4] # MM
        if len(original_digits) > 4: formatted_text += "/" + original_digits[4:8] # AAAA (até 8 dígitos no total)

        self.data_var.set(formatted_text)
        
        entry_widget = self.entries.get("Data")
        if entry_widget:
            # Usar after_idle para garantir que o cursor vá para o final
            entry_widget.after_idle(entry_widget.icursor, tk.END)

        self._data_var_trace_active = True # Reabilita o trace

    def _validate_time_action(self, action_code, text_being_inserted):
        if action_code == '0': return True
        if action_code == '1':
            if not text_being_inserted.isdigit(): return False
            current_digits_in_var = "".join(filter(str.isdigit, self.horario_var.get()))
            num_new_digits = len("".join(filter(str.isdigit, text_being_inserted)))
            if len(current_digits_in_var) + num_new_digits > 4: return False # HHMM = 4 dígitos
            return True
        return True

    def _format_time_trace(self, var_name, index, mode):
        if not self._horario_var_trace_active: return
        self._horario_var_trace_active = False
        
        current_text = self.horario_var.get()
        original_digits = "".join(filter(str.isdigit, current_text))
        
        formatted_text = ""
        if len(original_digits) > 0: formatted_text = original_digits[0:2] # HH
        if len(original_digits) > 2: formatted_text += ":" + original_digits[2:4] # MM
        
        self.horario_var.set(formatted_text)

        entry_widget = self.entries.get("Horário")
        if entry_widget:
            # Usar after_idle para garantir que o cursor vá para o final
            entry_widget.after_idle(entry_widget.icursor, tk.END)
            
        self._horario_var_trace_active = True # Reabilita o trace

    def _create_widgets(self):
        self.labels = {}
        self.entries = {}
        # Atualizando lista de campos
        fields = ["Nome", "Telefone", "Email", "Data (DD/MM/AAAA)", "Horário (HH:MM)", "Valor (R$)", "Serviço"]
        
        current_row = 0 # Para controlar a linha no grid
        for field_config in fields:
            label_text_full = field_config # ex: "Data (DD/MM/AAAA)"
            label_text_key = field_config.split('(')[0].strip() # ex: "Data"
            
            self.labels[label_text_key] = ttk.Label(self.form_frame, text=f"{label_text_full}:")
            self.labels[label_text_key].grid(row=current_row, column=0, padx=5, pady=5, sticky=tk.W)
            
            entry_widget = None
            if label_text_key == "Data":
                entry_widget = ttk.Entry(self.form_frame, width=40, 
                                                     textvariable=self.data_var,
                                                     validate='key', 
                                                     validatecommand=self.vcmd_date_action)
            elif label_text_key == "Horário": # Novo campo Horário
                entry_widget = ttk.Entry(self.form_frame, width=40,
                                                     textvariable=self.horario_var,
                                                     validate='key',
                                                     validatecommand=self.vcmd_time_action)
            else:
                entry_widget = ttk.Entry(self.form_frame, width=40)

            entry_widget.grid(row=current_row, column=1, padx=5, pady=5, sticky=tk.W)
            self.entries[label_text_key] = entry_widget # Armazena a referência

            if label_text_key == "Telefone":
                entry_widget.config(validate='key', validatecommand=self.vcmd_digits)
            elif label_text_key == "Valor":
                entry_widget.config(validate='key', validatecommand=self.vcmd_decimal)
            current_row += 1
        
        self.form_button_frame = ttk.Frame(self.form_frame)
        self.form_button_frame.grid(row=current_row, column=0, columnspan=2, pady=10) # Usa current_row

        self.add_button = ttk.Button(self.form_button_frame, text="Adicionar Novo", command=self._handle_add_click)
        self.save_button = ttk.Button(self.form_button_frame, text="Salvar Alterações", command=self._handle_save_click)
        self.clear_button = ttk.Button(self.form_button_frame, text="Limpar Campos", command=self._handle_clear_click)

        self.add_button.pack(side=tk.LEFT, padx=5)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        self.save_button.config(state=tk.DISABLED)

        self.tree = ttk.Treeview(self.list_frame, 
                                 columns=("ID", "Nome", "Data/Hora", "Serviço", "Valor"), # Mantido "Data/Hora"
                                 show='headings')
                                 
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome Cliente")
        self.tree.heading("Data/Hora", text="Data/Hora") # Label da coluna no Treeview
        self.tree.heading("Serviço", text="Serviço")
        self.tree.heading("Valor", text="Valor (R$)")

        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("Data/Hora", width=150, anchor=tk.CENTER) # Largura para DD/MM/AAAA HH:MM
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
            db_datetime_str = row[4] 
            display_datetime_tree = db_datetime_str 
            try:
                dt_obj = datetime.strptime(db_datetime_str, "%Y-%m-%d %H:%M:%S")
                display_datetime_tree = dt_obj.strftime("%d/%m/%Y %H:%M")
            except (ValueError, TypeError): 
                try:
                    dt_obj = datetime.strptime(db_datetime_str.split(" ")[0], "%Y-%m-%d")
                    display_datetime_tree = dt_obj.strftime("%d/%m/%Y")
                except (ValueError, TypeError, AttributeError):
                    pass 

            display_row = (row[0], row[1], display_datetime_tree, row[6], f"{row[5]:.2f}") 
            self.tree.insert("", tk.END, values=display_row, iid=row[0])

    def get_form_data(self):
        return {
            "Nome": self.entries["Nome"].get(),
            "Telefone": self.entries["Telefone"].get(),
            "Email": self.entries["Email"].get(),
            "Data": self.data_var.get(), 
            "Horário": self.horario_var.get(), 
            "Valor": self.entries["Valor"].get(),
            "Serviço": self.entries["Serviço"].get(),
        }

    def set_form_data(self, data_dict_from_controller): 
        self.clear_form_fields()
        self.entries["Nome"].insert(0, data_dict_from_controller.get("Nome", ""))
        self.entries["Telefone"].insert(0, data_dict_from_controller.get("Telefone", ""))
        self.entries["Email"].insert(0, data_dict_from_controller.get("Email", ""))
        
        db_datetime_str = data_dict_from_controller.get("Data", "") 
        display_date_form = ""
        display_time_form = ""
        if db_datetime_str:
            try:
                dt_obj = datetime.strptime(db_datetime_str, "%Y-%m-%d %H:%M:%S")
                display_date_form = dt_obj.strftime("%d/%m/%Y")
                display_time_form = dt_obj.strftime("%H:%M")
            except (ValueError, TypeError):
                try:
                    dt_obj = datetime.strptime(db_datetime_str.split(" ")[0], "%Y-%m-%d")
                    display_date_form = dt_obj.strftime("%d/%m/%Y")
                except (ValueError, TypeError, AttributeError):
                    display_date_form = "Data Inv." 
                    display_time_form = "Hora Inv."
        self.data_var.set(display_date_form)
        self.horario_var.set(display_time_form) 

        self.entries["Valor"].insert(0, data_dict_from_controller.get("Valor", ""))
        self.entries["Serviço"].insert(0, data_dict_from_controller.get("Serviço", ""))

    def clear_form_fields(self):
        for key, entry_widget in self.entries.items():
            if key == "Data":
                self.data_var.set("")
            elif key == "Horário": 
                self.horario_var.set("")
            else:
                entry_widget.delete(0, tk.END)
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

