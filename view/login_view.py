# view/login_view.py

import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    """
    Janela de Login da aplicação.
    """
    def __init__(self, master, controller):
        """
        Inicializa a LoginView.

        Args:
            master: A janela raiz (Tk) da aplicação.
            controller: O objeto AppController (ou um Mock) para comunicação.
        """
        self.master = master
        self.controller = controller

        # Cria uma Toplevel window para o login
        self.window = tk.Toplevel(self.master)
        self.window.title("Login - Salão de Beleza Neide Leila")
        self.window.geometry("300x150+500+300")      # Largura x Altura + Posição X + Posição Y
        self.window.resizable(False, False)

        # Frame principal
        self.frame = ttk.Frame(self.window, padding="20")
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Widgets
        self.label_user = ttk.Label(self.frame, text="Nome de Usuário:")
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.login_button = ttk.Button(self.frame, text="Entrar")

        # Layout
        self.label_user.pack(pady=5)
        self.username_entry.pack(pady=5)
        self.login_button.pack(pady=10)

        # Foca no campo de usuário ao abrir
        self.username_entry.focus_set()

        # Verifica se o controller não é None antes de configurar comandos
        if self.controller:
            self.username_entry.bind("<Return>", self.controller.handle_login_event)
            self.login_button.config(command=self.controller.handle_login_event)
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing) # Só define se houver controller real
        else:
            # Comportamento padrão para teste (ou pode ser configurado no teste)
            self.window.protocol("WM_DELETE_WINDOW", self.destroy)


    def get_username(self):
        """Retorna o nome de usuário inserido."""
        return self.username_entry.get()

    def show(self):
        """Mostra a janela de login."""
        self.window.deiconify()
        self.window.grab_set()

    def hide(self):
        """Esconde a janela de login."""
        self.window.withdraw()

    def destroy(self):
        """Destroi a janela de login."""
        # self.window.grab_release() # Cuidar ao chamar sem ter grab_set()
        self.window.destroy()

    def show_error(self, title, message):
        """Exibe uma mensagem de erro."""
        messagebox.showerror(title, message, parent=self.window)

    def on_closing(self):
        """Ação ao tentar fechar a janela de login (ex: fechar a aplicação)."""
        if messagebox.askokcancel("Sair", "Deseja sair da aplicação?", parent=self.window):
            self.master.destroy()
