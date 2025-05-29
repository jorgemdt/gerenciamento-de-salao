import tkinter as tk
from controller.app_controller import AppController

if __name__ == "__main__":
    # Cria a janela raiz da aplicação Tkinter
    root = tk.Tk()
    
    # Esconde a janela raiz inicialmente, pois o controller
    # decidirá qual view mostrar primeiro (LoginView como Toplevel)
    root.withdraw() 

    # Cria uma instância do nosso AppController, passando a janela raiz
    app = AppController(root)
    
    # Chama o método que inicia a lógica da aplicação (configura DB, mostra login)
    app.start_app()
    
    # Inicia o loop principal do Tkinter, que mantém a interface gráfica
    # ativa e responsiva a eventos até que a janela seja fechada.
    root.mainloop()

    print("Aplicação encerrada.")