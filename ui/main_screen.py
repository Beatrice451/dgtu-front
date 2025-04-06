import customtkinter as ctk
from api.task import TaskAPIClient
from tkcalendar import DateEntry
from datetime import datetime

class MainScreen(ctk.CTkFrame):
    def __init__(self, master, user_api_client):
        super().__init__(master)
        self.user_api_client = user_api_client
        self.task_api_client = TaskAPIClient(token=self.user_api_client.get_token())

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.task_list_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.task_list_frame.pack(side="left", fill="y")
        self.task_list_frame.pack_propagate(False)

        self.search_frame = ctk.CTkFrame(self.task_list_frame)
        self.search_frame.pack(fill="x", padx=5, pady=5)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search")
        self.search_entry.pack(fill="x", padx=5, pady=5)
        self.search_entry.bind("<Return>", lambda event: self.search_tasks())

        self.add_task_button = ctk.CTkButton(self.task_list_frame, text="+", width=40, height=40, command=self.show_task_creation_form)
        self.add_task_button.pack(side="bottom", pady=10, padx=10, anchor="sw")

        self.details_frame = ctk.CTkFrame(self.main_frame)
        self.details_frame.pack(side="right", fill="both", expand=True)

        # Инициализация меток для подробностей задачи
        self.task_title_author_frame = ctk.CTkFrame(self.details_frame)
        self.task_title_author_frame.pack(fill="x", padx=10, pady=5)

        self.task_title = ctk.CTkLabel(self.task_title_author_frame, text="Select a task", font=("Arial", 18, "bold"))
        self.task_title.pack(side="left", anchor="w")

        self.author_label = ctk.CTkLabel(self.task_title_author_frame, text="", font=("Arial", 12))
        self.author_label.pack(side="right", anchor="e")

        self.task_description = ctk.CTkLabel(self.details_frame, text="", wraplength=400, justify="left")
        self.task_description.pack(anchor="w", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.details_frame, text="", font=("Arial", 12))
        self.status_label.pack(anchor="w", padx=10, pady=5)

        self.deadline_label = ctk.CTkLabel(self.details_frame, text="", font=("Arial", 12))
        self.deadline_label.pack(anchor="w", padx=10, pady=5)

        self.created_at_label = ctk.CTkLabel(self.details_frame, text="", font=("Arial", 12))
        self.created_at_label.pack(anchor="w", padx=10, pady=5)

        self.tags_label = ctk.CTkLabel(self.details_frame, text="", font=("Arial", 12))
        self.tags_label.pack(anchor="w", padx=10, pady=5)

        self.delete_button = ctk.CTkButton(self.details_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side="bottom", anchor="se", padx=10, pady=10)

        self.load_tasks()

    def load_tasks(self, name_filter=None):
        response = self.task_api_client.get_tasks(name=name_filter) if name_filter else self.task_api_client.get_tasks()
        if response.status_code == 200:
            tasks = response.json()

            for widget in self.task_list_frame.winfo_children():
                if widget != self.search_frame and widget != self.add_task_button:
                    widget.destroy()

            for task in tasks:
                task_frame = ctk.CTkFrame(self.task_list_frame, height=50, corner_radius=0, fg_color="transparent", border_width=0)
                task_frame.pack(fill="x", pady=0)

                task_label = ctk.CTkLabel(task_frame, text=task["name"], font=("Arial", 14), text_color="white", padx=10, pady=2, anchor="w")
                task_label.pack(fill="x", padx=0, pady=0, anchor="w")

                truncated_description = (task["description"][:40] + "...") if len(task["description"]) > 40 else task["description"]
                task_desc_label = ctk.CTkLabel(task_frame, text=truncated_description, font=("Arial", 12), text_color="gray", padx=10, pady=0, anchor="w")
                task_desc_label.pack(fill="x", padx=0, pady=0, anchor="w")

                separator = ctk.CTkFrame(self.task_list_frame, height=1, fg_color="gray")
                separator.pack(fill="x", padx=5, pady=2)

                task_label.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))
                task_desc_label.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))

    def search_tasks(self):
        name_filter = self.search_entry.get()
        self.load_tasks(name_filter)

    def show_task_creation_form(self):
        # Скрываем элементы для отображения подробностей задачи
        self.hide_task_details()

        for widget in self.details_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.pack_forget()

        name_entry = ctk.CTkEntry(self.details_frame, placeholder_text="Task Name")
        name_entry.pack(fill="x", padx=10, pady=5)

        description_entry = ctk.CTkEntry(self.details_frame, placeholder_text="Task Description")
        description_entry.pack(fill="x", padx=10, pady=5)

        status_options = ["todo", "in_progress", "done"]
        status_entry = ctk.CTkComboBox(self.details_frame, values=status_options)
        status_entry.pack(fill="x", padx=10, pady=5)

        deadline_date_entry = DateEntry(self.details_frame)
        deadline_date_entry.pack(fill="x", padx=10, pady=5)

        deadline_time_entry = ctk.CTkEntry(self.details_frame, placeholder_text="HH:MM")
        deadline_time_entry.pack(fill="x", padx=10, pady=5)

        response = self.task_api_client.get_tags()
        if response.status_code == 200:
            tags = response.json()
            self.tag_vars = {}
            for tag in tags:
                var = ctk.BooleanVar()
                checkbox = ctk.CTkCheckBox(self.details_frame, text=tag["name"], variable=var)
                checkbox.pack(anchor="w", padx=10)
                self.tag_vars[tag["id"]] = var

        submit_button = ctk.CTkButton(self.details_frame, text="Create Task", command=lambda: self.create_task(name_entry, description_entry, status_entry, deadline_date_entry, deadline_time_entry))
        submit_button.pack(pady=10)

    def create_task(self, name_entry, description_entry, status_entry, deadline_date_entry, deadline_time_entry):
        selected_tags = [tag_id for tag_id, var in self.tag_vars.items() if var.get()]
        deadline_date = deadline_date_entry.get_date().strftime("%Y-%m-%d")
        deadline_time = deadline_time_entry.get().strip() or "00:00"

        try:
            deadline_datetime = datetime.strptime(f"{deadline_date} {deadline_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            deadline_datetime = datetime.strptime(f"{deadline_date} 00:00", "%Y-%m-%d %H:%M")

        task_data = {
            "name": name_entry.get(),
            "description": description_entry.get(),
            "status": status_entry.get(),
            "deadline": deadline_datetime.isoformat(),
            "tags": selected_tags
        }
        self.task_api_client.create_task(task_data)
        self.load_tasks()

        # Скрыть форму создания задачи после создания
        self.hide_task_creation_form()

    def show_task_details(self, task):
        # Обновляем информацию о таске на правой панели
        self.task_title.configure(text=task["name"])
        self.author_label.configure(text=f"Author: {task.get('author', 'N/A')}")
        self.task_description.configure(text=task["description"])
        self.status_label.configure(text=f"Status: {task['status']}")
        self.deadline_label.configure(text=f"Deadline: {task['deadline']}")
        self.created_at_label.configure(text=f"Created At: {task['createdAt']}")
        # Форматируем теги как строку
        tags = ", ".join(task["tags"])
        self.tags_label.configure(text=f"Tags: {tags}") 
        self.selected_task = task  # Сохраняем выбранную задачу для удаления

        # Показываем элементы для отображения подробностей задачи
        self.show_task_details_ui()

    def delete_task(self):
        if hasattr(self, 'selected_task'):
            task_id = self.selected_task["id"]
            response = self.task_api_client.delete_task(task_id)
            if response.status_code == 200:
                self.load_tasks()  # Перезагружаем список задач
                self.hide_task_details()  # Скрываем детали после удаления
            else:
                print("Error deleting task:", response.text)

    def hide_task_details(self):
        for widget in self.details_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.pack_forget()
        self.delete_button.pack_forget()

    def show_task_details_ui(self):
        self.task_title.pack(side="left", anchor="w")
        self.author_label.pack(side="right", anchor="e")
        self.task_description.pack(anchor="w", padx=10, pady=5)
        self.status_label.pack(anchor="w", padx=10, pady=5)
        self.deadline_label.pack(anchor="w", padx=10, pady=5)
        self.created_at_label.pack(anchor="w", padx=10, pady=5)
        self.tags_label.pack(anchor="w", padx=10, pady=5)
        self.delete_button.pack(side="bottom", anchor="se", padx=10, pady=10)

    def hide_task_creation_form(self):
        for widget in self.details_frame.winfo_children():
            if isinstance(widget, (ctk.CTkEntry, ctk.CTkComboBox, ctk.CTkCheckBox, DateEntry)):
                widget.pack_forget()
        for widget in self.details_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.pack_forget()
