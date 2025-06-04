import tkinter as tk
from datetime import datetime
from model.database import setup_database
from model.agendamento import AgendamentoModel
from model.user_model import UserModel 
from view.login_view import LoginView
from view.main_view import MainView
from view.report_view import ReportView
from view.registration_view import RegistrationView

class AppController:
    """Controller principal da aplicação, gerenciando Models e Views."""
    def __init__(self, master):
        """Inicializa o Controller, Models e referências de Views."""
        self.master = master
        self.agendamento_model = AgendamentoModel() 
        self.user_model = UserModel()
        self.login_view = None
        self.main_view = None
        self.report_view = None
        self.registration_view = None 
        self.selected_id = None

    def start_app(self):
        """Inicia a aplicação: configura DB e decide entre login ou registro."""
        print("Iniciando setup do banco de dados...")
        setup_database()
        if not self.user_model.has_users():
            print("Nenhum usuário. Mostrando tela de cadastro do administrador...")
            self.registration_view = RegistrationView(self.master, self)
        else:
            print("Usuários encontrados. Mostrando tela de login...")
            self.login_view = LoginView(self.master, self)

    def handle_first_user_registration(self):
        """Processa o cadastro do primeiro usuário administrador."""
        if self.registration_view is None or not self.registration_view.window.winfo_exists():
            return
        details = self.registration_view.get_details()
        username, password, confirm_password = details["username"], details["password"], details["confirm_password"]
        if not username or not password:
            self.registration_view.show_error("Erro", "Usuário e senha são obrigatórios.")
            return
        if password != confirm_password:
            self.registration_view.show_error("Erro", "As senhas não coincidem.")
            return
        success, message = self.user_model.create_user(username, password)
        if success:
            self.registration_view.show_message("Sucesso", message)
            self.registration_view.destroy()
            self.login_view = LoginView(self.master, self)
        else:
            self.registration_view.show_error("Erro de Cadastro", message)

    def handle_login_event(self, event=None):
        """Processa a tentativa de login do usuário."""
        if self.login_view is None or not self.login_view.window.winfo_exists():
            return
        username, password_to_check = self.login_view.get_credentials()
        if not username or not password_to_check:
            self.login_view.show_error("Login Inválido", "Usuário e senha são obrigatórios.")
            return
        if self.user_model.check_credentials(username, password_to_check):
            self.login_view.destroy()
            self.show_main_view()
        else:
            self.login_view.show_error("Login Falhou", "Usuário ou senha incorretos.")
            
    def show_main_view(self):
        """Cria e exibe a MainView e carrega os dados iniciais."""
        self.main_view = MainView(self.master, self)
        self.main_view.show()
        self.load_data_to_main_view()

    def load_data_to_main_view(self):
        """Busca agendamentos do Model e atualiza a Treeview na MainView."""
        data = self.agendamento_model.get_all_agendamentos()
        self.main_view.populate_treeview(data)
        self.main_view.clear_form() 
        self.selected_id = None

    def handle_tree_select(self, event=None):
        """Lida com a seleção de um item na Treeview da MainView."""
        self.selected_id = self.main_view.get_selected_item_id()
        if self.selected_id:
            self.main_view.enable_edit_delete_buttons(True)
            self.main_view.enable_save_button(False) 
        else:
            self.main_view.enable_edit_delete_buttons(False)

    def handle_edit_selection(self):
        """Carrega dados do item selecionado para o formulário de edição."""
        if not self.selected_id: return
        ag_data_tuple = self.agendamento_model.get_agendamento_by_id(self.selected_id)
        if ag_data_tuple:
            data_dict = {
                "Nome": ag_data_tuple[1], "Telefone": ag_data_tuple[2], "Email": ag_data_tuple[3],
                "Data": ag_data_tuple[4], "Valor": f"{ag_data_tuple[5]:.2f}", "Serviço": ag_data_tuple[6],
            }
            self.main_view.set_form_data(data_dict)
            self.main_view.enable_save_button(True) 
            self.main_view.enable_edit_delete_buttons(False) 
        else:
            self.main_view.show_error("Erro", "Agendamento não encontrado.")
            self.load_data_to_main_view()

    def _validate_and_get_data(self):
        """Valida dados do formulário e formata data/hora para o banco."""
        form_data = self.main_view.get_form_data()
        if not all(form_data.get(key) for key in ["Nome", "Serviço", "Data", "Horário"]):
            self.main_view.show_error("Campos Obrigatórios", "Nome, Serviço, Data e Horário são obrigatórios.")
            return None
        try:
            form_data["Valor"] = float(form_data["Valor"]) if form_data["Valor"] else 0.0
        except ValueError:
            self.main_view.show_error("Valor Inválido", "Valor deve ser numérico (ex: 50.00).")
            return None
        try:
            parsed_date = datetime.strptime(form_data["Data"], "%d/%m/%Y")
            parsed_time = datetime.strptime(form_data["Horário"], "%H:%M")
            combined_dt = datetime.combine(parsed_date.date(), parsed_time.time())
            form_data["Data"] = combined_dt.strftime("%Y-%m-%d %H:%M:00")
            if "Horário" in form_data: del form_data["Horário"]
        except ValueError:
            self.main_view.show_error("Data/Horário Inválido", "Use DD/MM/AAAA e HH:MM válidos.")
            return None
        return form_data

    def handle_add_agendamento(self):
        """Processa a adição de um novo agendamento."""
        data_to_add = self._validate_and_get_data() 
        if data_to_add is None: return 
        success = self.agendamento_model.add_agendamento(
            data_to_add["Nome"], data_to_add["Telefone"], data_to_add["Email"],
            data_to_add["Data"], data_to_add["Valor"], data_to_add["Serviço"] 
        )
        if success:
            self.main_view.show_message("Sucesso", "Agendamento adicionado!")
            self.load_data_to_main_view()
        else:
            self.main_view.show_error("Erro", "Não foi possível adicionar.")

    def handle_update_agendamento(self):
        """Processa a atualização de um agendamento existente."""
        if not self.selected_id:
            self.main_view.show_error("Erro", "Nenhum agendamento selecionado.")
            return
        data_to_update = self._validate_and_get_data() 
        if data_to_update is None: return 
        success = self.agendamento_model.update_agendamento(
            self.selected_id, data_to_update["Nome"], data_to_update["Telefone"], 
            data_to_update["Email"], data_to_update["Data"], 
            data_to_update["Valor"], data_to_update["Serviço"] 
        )
        if success:
            self.main_view.show_message("Sucesso", "Agendamento atualizado!")
            self.load_data_to_main_view()
        else:
            self.main_view.show_error("Erro", "Não foi possível atualizar.")

    def handle_delete_agendamento(self):
        """Processa a remoção de um agendamento."""
        if not self.selected_id:
            self.main_view.show_error("Erro", "Nenhum agendamento selecionado.")
            return
        if self.main_view.ask_question("Confirmar", "Remover este agendamento?"):
            success = self.agendamento_model.delete_agendamento(self.selected_id)
            if success:
                self.main_view.show_message("Sucesso", "Agendamento removido!")
                self.load_data_to_main_view()
            else:
                self.main_view.show_error("Erro", "Não foi possível remover.")

    def handle_show_report(self):
        """Cria e exibe a janela de relatório com todos os agendamentos."""
        if self.report_view is None or not self.report_view.window.winfo_exists():
            self.report_view = ReportView(self.master, self)
        data = self.agendamento_model.get_all_agendamentos()
        self.report_view.populate_report(data)
        self.report_view.show()
        self.report_view.window.lift() 

    def handle_clear_form_request(self):
        """Lida com a solicitação da View para limpar o formulário e resetar estado."""
        self.selected_id = None
        if self.main_view: 
            self.main_view.enable_save_button(False)
            self.main_view.enable_edit_delete_buttons(False)
            self.main_view.add_button.config(state=tk.NORMAL)