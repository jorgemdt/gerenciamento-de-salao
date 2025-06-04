import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    """Representa a janela de Login da aplicação."""
    def __init__(self, master, controller):
        """Inicializa a LoginView com seus widgets e configurações."""
        self.master = master
        self.controller = controller

        self.window = tk.Toplevel(self.master)
        self.window.title("Login - Salão de Beleza Neide Leila")
        self.window.geometry("350x200+500+300") 
        self.window.resizable(False, False)

        self.frame = ttk.Frame(self.window, padding="20")
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        style = ttk.Style(self.window)
        style.configure("Login.TButton", padding=[10, 5, 10, 5])

        self.label_user = ttk.Label(self.frame, text="Nome de Usuário:")
        self.username_entry = ttk.Entry(self.frame, width=35)
        
        self.label_password = ttk.Label(self.frame, text="Senha:")
        self.password_entry = ttk.Entry(self.frame, width=35, show="*")

        self.login_button = ttk.Button(self.frame, text="Entrar")

        self.label_user.pack(pady=(0,5))
        self.username_entry.pack(pady=5)
        self.label_password.pack(pady=(10,5))
        self.password_entry.pack(pady=5)
        self.login_button.pack(pady=1) 

        self.username_entry.focus_set()

        if self.controller:
            self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
            self.password_entry.bind("<Return>", self.controller.handle_login_event)
            self.login_button.config(command=self.controller.handle_login_event)
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        else: 
            self.window.protocol("WM_DELETE_WINDOW", self.destroy)

    def get_credentials(self):
        """Retorna o nome de usuário e a senha inseridos."""
        return self.username_entry.get(), self.password_entry.get()

    def show(self):
        """Mostra a janela de login e a torna modal."""
        self.window.deiconify()
        self.window.grab_set() 

    def hide(self):
        """Esconde a janela de login."""
        self.window.withdraw()

    def destroy(self):
        """Destroi a janela de login."""
        if self.window.winfo_exists():
            try:
                self.window.grab_release()
            except tk.TclError:
                pass
            self.window.destroy()

    def show_error(self, title, message):
        """Exibe uma mensagem de erro na janela de login."""
        messagebox.showerror(title, message, parent=self.window)

    def on_closing(self):
        """Ação ao tentar fechar a janela de login."""
        if messagebox.askokcancel("Sair", "Deseja sair da aplicação?", parent=self.window):
            self.master.destroy()