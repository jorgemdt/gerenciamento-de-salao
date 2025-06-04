import tkinter as tk
from tkinter import ttk, messagebox

class RegistrationView:
    """Representa a janela de Cadastro do Primeiro Usuário."""
    def __init__(self, master, controller):
        """Inicializa a RegistrationView com seus widgets e configurações."""
        self.master = master
        self.controller = controller

        self.window = tk.Toplevel(self.master)
        self.window.title("Cadastro do Primeiro Usuário")
        self.window.geometry("400x320+450+250") 
        self.window.resizable(False, False)
        self.window.grab_set() 

        self.frame = ttk.Frame(self.window, padding="20")
        self.frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(self.frame, text="Bem-vindo! Por favor, cadastre o usuário administrador.").pack(pady=(0,10))

        self.label_user = ttk.Label(self.frame, text="Nome de Usuário:")
        self.username_entry = ttk.Entry(self.frame, width=35)
        
        self.label_password = ttk.Label(self.frame, text="Senha:")
        self.password_entry = ttk.Entry(self.frame, width=35, show="*")
        
        self.label_confirm_password = ttk.Label(self.frame, text="Confirmar Senha:")
        self.confirm_password_entry = ttk.Entry(self.frame, width=35, show="*")

        self.register_button = ttk.Button(self.frame, text="Cadastrar Administrador")

        self.label_user.pack(pady=5)
        self.username_entry.pack(pady=5)
        self.label_password.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.label_confirm_password.pack(pady=5)
        self.confirm_password_entry.pack(pady=5)
        self.register_button.pack(pady=10) 

        self.username_entry.focus_set()
        
        if self.controller:
            self.register_button.config(command=self.controller.handle_first_user_registration)
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing_critical)
        else: 
            self.window.protocol("WM_DELETE_WINDOW", self.destroy)

    def get_details(self):
        """Retorna os detalhes inseridos no formulário de cadastro."""
        return {
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
            "confirm_password": self.confirm_password_entry.get()
        }

    def show_message(self, title, message):
        """Exibe uma mensagem informativa na janela de cadastro."""
        messagebox.showinfo(title, message, parent=self.window)

    def show_error(self, title, message):
        """Exibe uma mensagem de erro na janela de cadastro."""
        messagebox.showerror(title, message, parent=self.window)

    def destroy(self):
        """Destroi a janela de cadastro."""
        if self.window.winfo_exists():
            try:
                self.window.grab_release()
            except tk.TclError:
                pass
            self.window.destroy()

    def on_closing_critical(self):
        """Ação ao tentar fechar a janela crítica de cadastro."""
        if messagebox.askyesno("Atenção!", 
                               "É necessário cadastrar um administrador para usar o sistema.\n"
                               "Deseja realmente sair sem cadastrar? A aplicação será encerrada.",
                               icon='warning', parent=self.window):
            self.master.destroy()