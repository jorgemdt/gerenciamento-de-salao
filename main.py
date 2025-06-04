import tkinter as tk
from controller.app_controller import AppController

if __name__ == "__main__":
    """Ponto de entrada principal da aplicação."""
    root = tk.Tk()
    root.withdraw() 
    app = AppController(root)
    app.start_app()
    root.mainloop()
    print("Aplicação encerrada.")