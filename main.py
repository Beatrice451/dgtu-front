import customtkinter as ctk
from api.user import UserAPIClient
from ui.login_screen import LoginScreen
from ui.register_screen import RegisterScreen
from ui.main_screen import MainScreen

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Всё идёт по плану")
        self.geometry("1200x700")
        
        self.api_client = UserAPIClient()
        self.show_login_screen()
    
    def show_login_screen(self):
        self.clear_screen()
        self.login_screen = LoginScreen(self, self.api_client, self.show_register_screen, self.show_main_screen)
        self.login_screen.pack(expand=True)
    
    def show_register_screen(self):
        
        self.clear_screen()
        self.register_screen = RegisterScreen(self, self.api_client, self.show_login_screen)
        self.register_screen.pack(expand=True)
    
    def show_main_screen(self):
        self.clear_screen()
        self.main_screen = MainScreen(self, self.api_client)
        self.main_screen.pack(fill="both", expand=True)
    
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
