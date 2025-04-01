import customtkinter as ctk

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, api_client, show_register_screen, show_main_screen):
        super().__init__(master)
        self.api_client = api_client
        self.show_register_screen = show_register_screen
        self.show_main_screen = show_main_screen
        
        self.label = ctk.CTkLabel(self, text="Login", font=("Arial", 20, "bold"))
        self.label.pack(pady=10)
        
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=5)
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)
        
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
        self.register_button = ctk.CTkButton(self, text="Register", command=self.show_register_screen)
        self.register_button.pack()
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        response = self.api_client.login(email, password)
        
        if response.status_code == 200:
            self.show_main_screen()
        else:
            self.error_label.configure(text="Invalid email or password")
