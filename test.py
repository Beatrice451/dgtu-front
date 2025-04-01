import customtkinter as ctk
from api.user import UserAPIClient

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("800x500")
        
        self.api_client = UserAPIClient()
        self.show_login_screen()
    
    def show_login_screen(self):
        self.clear_screen()
        
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True)
        
        ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.username_entry.pack(pady=5)
        
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)
        
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=5)
        
        self.switch_to_register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.show_register_screen)
        self.switch_to_register_button.pack(pady=5)
    
    def login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()
        response = self.api_client.login(email, password)
        
        if response.status_code == 200:
            self.show_main_screen()
        else:
            print("Login failed")
    
    def show_register_screen(self):
        self.clear_screen()
        
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(expand=True)
        
        ctk.CTkLabel(self.register_frame, text="Register", font=("Arial", 18, "bold")).pack(pady=10)
        self.new_email_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Email")
        self.new_email_entry.pack(pady=5)
        
        self.new_name_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Name")
        self.new_name_entry.pack(pady=5)
        
        self.new_city_entry = ctk.CTkEntry(self.register_frame, placeholder_text="City")
        self.new_city_entry.pack(pady=5)
        
        self.new_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.new_password_entry.pack(pady=5)
        
        self.confirm_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.pack(pady=5)
        
        self.register_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register)
        self.register_button.pack(pady=5)
        
        self.switch_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=self.show_login_screen)
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
            self.show_login_screen()
        else:
            print("Registration failed")
    
    def show_main_screen(self):
        self.clear_screen()
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.task_list_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.task_list_frame.pack(side="left", fill="y")
        
        self.search_entry = ctk.CTkEntry(self.task_list_frame, placeholder_text="Search")
        self.search_entry.pack(fill="x", padx=5, pady=5)
        
        self.task_listbox = ctk.CTkTextbox(self.task_list_frame, width=250, wrap="word")
        self.task_listbox.pack(fill="both", expand=True)
        
        self.details_frame = ctk.CTkFrame(self.main_frame)
        self.details_frame.pack(side="right", fill="both", expand=True)
        
        self.task_title = ctk.CTkLabel(self.details_frame, text="Very important task #1", font=("Arial", 18, "bold"))
        self.task_title.pack(anchor="w", padx=10, pady=5)
        
        self.task_description = ctk.CTkLabel(self.details_frame, text="Description of the selected task...", wraplength=400, justify="left")
        self.task_description.pack(anchor="w", padx=10, pady=5)
        
        self.author_label = ctk.CTkLabel(self.details_frame, text="Author: Beatrice", font=("Arial", 12))
        self.author_label.pack(anchor="w", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(self.details_frame, text="Status: In Progress", font=("Arial", 12))
        self.status_label.pack(anchor="w", padx=10, pady=5)
        
        self.populate_tasks()
    
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def populate_tasks(self):
        for i in range(7):
            self.task_listbox.insert("end", f"Very important task #{i+1}\nDescription of task...\n\n")

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
