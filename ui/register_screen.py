import customtkinter as ctk


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master, api_client, show_login):
        super().__init__(master)
        self.api_client = api_client
        self.show_login = show_login
        
        ctk.CTkLabel(self, text="Register", font=("Arial", 18, "bold")).pack(pady=10)
        self.new_email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.new_email_entry.pack(pady=5)
        
        self.new_name_entry = ctk.CTkEntry(self, placeholder_text="Name")
        self.new_name_entry.pack(pady=5)
        
        self.new_city_entry = ctk.CTkEntry(self, placeholder_text="City")
        self.new_city_entry.pack(pady=5)
        
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.new_password_entry.pack(pady=5)
        
        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.pack(pady=5)
        
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack(pady=5)
        
        self.switch_to_login_button = ctk.CTkButton(self, text="Back to Login", command=self.show_login)
        self.switch_to_login_button.pack(pady=5)
    
    def register(self):
        email = self.new_email_entry.get()
        name = self.new_name_entry.get()
        city = self.new_city_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if password != confirm_password:
            print("Passwords do not match!")
            return
        
        user_data = {"email": email, "name": name, "password": password, "city": city}
        response = self.api_client.create_user(user_data)
        if response.status_code == 201:
            self.show_login()
        else:
            print("Registration failed")