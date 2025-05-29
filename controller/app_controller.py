import tkinter as tk
from datetime import datetime # Adicionado import
from model.database import setup_database
from model.agendamento import AgendamentoModel, check_user
from view.login_view import LoginView
from view.main_view import MainView
from view.report_view import ReportView


class AppController:
    """
    O Controller principal da aplicação. Gerencia Models e Views.
    """
    def __init__(self, master):
        """
        Inicializa o Controller.

        Args:
            master: A janela raiz (Tk) da aplicação.
        """
        self.master = master
        self.model = AgendamentoModel()
        self.login_view = None
        self.main_view = None
        self.report_view = None
        self.selected_id = None # Armazena o ID do item selecionado na Treeview

    def start_app(self):
        """Inicia a aplicação: configura DB e mostra a tela de login."""
        print("Iniciando setup do banco de dados...")
        setup_database()
        print("Mostrando tela de login...")
        self.login_view = LoginView(self.master, self)
        # A janela raiz (master) está oculta, Toplevel aparecerá
        # O mainloop será chamado em main.py

    def handle_login_event(self, event=None):
        """
        Lida com o evento de login (botão ou Enter).
        Verifica o usuário e abre a tela principal se válido.
        """
        username = self.login_view.get_username()
        if not username:
            self.login_view.show_error("Login Inválido", "Por favor, digite um nome de usuário.")
            return

        print(f"Tentando login com: {username}")
        if check_user(username):
            print("Login bem-sucedido!")
            self.login_view.destroy() # Fecha a janela de login
            self.show_main_view()     # Mostra a janela principal
        else:
            print("Login falhou.")
            self.login_view.show_error("Login Falhou", f"Usuário '{username}' não encontrado.")
            
    def show_main_view(self):
        """Cria e exibe a MainView."""
        self.main_view = MainView(self.master, self)
        self.main_view.show() # Mostra a janela principal (que é a 'master')
        self.load_data_to_main_view() # Carrega os dados iniciais

    def load_data_to_main_view(self):
        """Busca os dados do Model e atualiza a Treeview na MainView."""
        print("Carregando dados para a MainView...")
        data = self.model.get_all_agendamentos()
        self.main_view.populate_treeview(data)
        self.main_view.clear_form() 
        self.selected_id = None

    def handle_tree_select(self, event=None):
        """
        Lida com a seleção de um item na Treeview.
        Habilita botões de Editar/Remover.
        """
        self.selected_id = self.main_view.get_selected_item_id()
        if self.selected_id:
            print(f"Item selecionado, ID: {self.selected_id}")
            self.main_view.enable_edit_delete_buttons(True)
            self.main_view.enable_save_button(False) 
        else:
            print("Nenhum item selecionado.")
            self.main_view.enable_edit_delete_buttons(False)

    def handle_edit_selection(self):
        """Carrega os dados do item selecionado para o formulário."""
        if not self.selected_id:
            return
            
        ag_data_tuple = self.model.get_agendamento_by_id(self.selected_id) # Renomeado para clareza
        if ag_data_tuple:
            # Converte a tupla (do DB) para um dicionário (para a View)
            # A MainView.set_form_data se encarregará de formatar a data de YYYY-MM-DD para DD/MM/AAAA
            data_dict = {
                "Nome": ag_data_tuple[1],
                "Telefone": ag_data_tuple[2],
                "Email": ag_data_tuple[3],
                "Data": ag_data_tuple[4], # Mantém formato YYYY-MM-DD HH:MM:SS do DB
                "Valor": f"{ag_data_tuple[5]:.2f}", 
                "Serviço": ag_data_tuple[6],
            }
            self.main_view.set_form_data(data_dict)
            self.main_view.enable_save_button(True) 
            self.main_view.enable_edit_delete_buttons(False) 
        else:
            self.main_view.show_error("Erro", "Agendamento não encontrado.")
            self.load_data_to_main_view() 

    def _validate_and_get_data(self):
        """Valida e obtém os dados do formulário, convertendo a data para o formato do DB."""
        form_data = self.main_view.get_form_data() # form_data["Data"] virá como DD/MM/AAAA
        
        # Validação básica de campos obrigatórios
        if not form_data["Nome"] or not form_data["Serviço"]: # Data será validada abaixo
            self.main_view.show_error("Campos Obrigatórios", "Nome e Serviço são obrigatórios.")
            return None
            
        try:
            valor = float(form_data["Valor"]) if form_data["Valor"] else 0.0
            form_data["Valor"] = valor 
        except ValueError:
            self.main_view.show_error("Valor Inválido", "O valor do serviço deve ser um número (ex: 50.00).")
            return None
        
        # Validação e conversão da Data
        date_str_ddmmyyyy = form_data["Data"] # Espera-se DD/MM/AAAA da view
        if not date_str_ddmmyyyy:
            self.main_view.show_error("Campo Obrigatório", "Data é obrigatória.")
            return None
        
        try:
            # Valida DD/MM/AAAA e converte para objeto datetime
            parsed_date = datetime.strptime(date_str_ddmmyyyy, "%d/%m/%Y")
            # Converte para YYYY-MM-DD HH:MM:SS para o banco (com hora padrão 00:00:00)
            form_data["Data"] = parsed_date.strftime("%Y-%m-%d") + " 00:00:00"
        except ValueError:
            self.main_view.show_error("Data Inválida",
                                      "A data deve estar no formato DD/MM/AAAA e ser uma data válida (ex: 29/05/2025).")
            return None
            
        return form_data # Retorna o dicionário com dados validados e data convertida para formato DB

    def handle_add_agendamento(self):
        """Lida com a adição de um novo agendamento."""
        data_to_add = self._validate_and_get_data() 
        if data_to_add is None: return 

        success = self.model.add_agendamento(
            data_to_add["Nome"], data_to_add["Telefone"], data_to_add["Email"],
            data_to_add["Data"], data_to_add["Valor"], data_to_add["Serviço"] # "Data" já está YYYY-MM-DD HH:MM:SS
        )
        if success:
            self.main_view.show_message("Sucesso", "Agendamento adicionado!")
            self.load_data_to_main_view()
        else:
            self.main_view.show_error("Erro", "Não foi possível adicionar o agendamento.")

    def handle_update_agendamento(self):
        """Lida com a atualização de um agendamento existente."""
        if not self.selected_id:
            self.main_view.show_error("Erro", "Nenhum agendamento selecionado para salvar.")
            return

        data_to_update = self._validate_and_get_data() 
        if data_to_update is None: return 

        success = self.model.update_agendamento(
            self.selected_id, data_to_update["Nome"], data_to_update["Telefone"], data_to_update["Email"],
            data_to_update["Data"], data_to_update["Valor"], data_to_update["Serviço"] # "Data" já está YYYY-MM-DD HH:MM:SS
        )
        if success:
            self.main_view.show_message("Sucesso", "Agendamento atualizado!")
            self.load_data_to_main_view()
        else:
            self.main_view.show_error("Erro", "Não foi possível atualizar o agendamento.")

    def handle_delete_agendamento(self):
        """Lida com a remoção de um agendamento."""
        if not self.selected_id:
            self.main_view.show_error("Erro", "Nenhum agendamento selecionado para remover.")
            return

        if self.main_view.ask_question("Confirmar Remoção", 
                                        "Tem certeza que deseja remover este agendamento?"):
            success = self.model.delete_agendamento(self.selected_id)
            if success:
                self.main_view.show_message("Sucesso", "Agendamento removido!")
                self.load_data_to_main_view()
            else:
                self.main_view.show_error("Erro", "Não foi possível remover o agendamento.")

    def handle_show_report(self):
        """Cria/mostra a janela de relatório."""
        print("Gerando relatório...")
        if self.report_view is None or not self.report_view.window.winfo_exists():
            self.report_view = ReportView(self.master, self)
        
        data = self.model.get_all_agendamentos()
        self.report_view.populate_report(data)
        self.report_view.show()
        self.report_view.window.lift() 

    def handle_clear_form(self): # Este método pode não ser mais chamado diretamente pela view
        """Lida com o botão Limpar."""
        # A view tem seu próprio clear_form. Este método é mais para o controller resetar estado.
        self.main_view.clear_form() # Chama o clear_form da view que reseta os botões também
        self.selected_id = None

    def handle_clear_form_request(self): # Chamado pela MainView
            """Lida com a solicitação da View para limpar o formulário."""
            print("Controller: Recebido pedido para limpar formulário.")
            # A view já limpa seus campos visuais e reseta botões via seu próprio clear_form.
            # Aqui, o controller apenas reseta seu estado interno.
            self.selected_id = None