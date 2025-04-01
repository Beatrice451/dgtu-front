import customtkinter as ctk
from api.task import TaskAPIClient

class MainScreen(ctk.CTkFrame):
    def __init__(self, master, user_api_client):
        super().__init__(master)
        self.user_api_client = user_api_client
        self.task_api_client = TaskAPIClient(token=self.user_api_client.get_token())

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.task_list_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.task_list_frame.pack(side="left", fill="y")
        self.task_list_frame.pack_propagate(False)  # Фиксированная ширина

        self.search_frame = ctk.CTkFrame(self.task_list_frame)
        self.search_frame.pack(fill="x", padx=5, pady=5)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search")
        self.search_entry.pack(fill="x", padx=5, pady=5)
        self.search_entry.bind("<Return>", lambda event: self.search_tasks())

        self.details_frame = ctk.CTkFrame(self.main_frame)
        self.details_frame.pack(side="right", fill="both", expand=True)

        # Панель для подробной информации о таске
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

        self.load_tasks()

    def load_tasks(self, name_filter=None):
        response = self.task_api_client.get_tasks_by_name(name=name_filter) if name_filter else self.task_api_client.get_tasks()
        if response.status_code == 200:
            tasks = response.json()

            # Очищаем старые элементы в панели
            for widget in self.task_list_frame.winfo_children():
                widget.destroy()

            # Поле поиска
            self.search_frame = ctk.CTkFrame(self.task_list_frame)
            self.search_frame.pack(fill="x", padx=5, pady=5)

            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search tasks...")
            self.search_entry.pack(fill="x", padx=5, pady=5)
            self.search_entry.insert(0, name_filter if name_filter else "")  # Сохраняем текст поиска
            self.search_entry.bind("<Return>", lambda event: self.search_tasks())

            # Создаём таски в виде прямоугольников без канваса
            for task in tasks:
                task_frame = ctk.CTkFrame(
                    self.task_list_frame,
                    height=50,
                    corner_radius=0,
                    fg_color="transparent",  # Прозрачный фон
                    border_width=0,
                )
                task_frame.pack(fill="x", pady=0)

                task_label = ctk.CTkLabel(
                    task_frame,
                    text=task["name"],  # Имя таска
                    font=("Arial", 14),
                    text_color="white",
                    padx=10,
                    pady=2,  # Уменьшенный отступ
                    anchor="w"  # Выравнивание текста по левому краю
                )
                task_label.pack(fill="x", padx=0, pady=0, anchor="w")

                # Добавляем описание таска (с обрезкой при длинном тексте)
                truncated_description = (task["description"][:40] + "...") if len(task["description"]) > 40 else task["description"]
                task_desc_label = ctk.CTkLabel(
                    task_frame,
                    text=truncated_description,
                    font=("Arial", 12),
                    text_color="gray",
                    padx=10,
                    pady=0,  # Уменьшенный отступ
                    anchor="w"
                )
                task_desc_label.pack(fill="x", padx=0, pady=0, anchor="w")

                # Добавляем разделительную линию
                separator = ctk.CTkFrame(self.task_list_frame, height=2, fg_color="gray")
                separator.pack(fill="x", padx=5, pady=2)

                # Добавляем событие на клик по таску
                task_label.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))
                task_desc_label.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))

    def search_tasks(self):
        name_filter = self.search_entry.get()
        self.load_tasks(name_filter)

    def show_task_details(self, task):
        # Обновляем информацию о таске на правой панели
        self.task_title.configure(text=task["name"])
        self.author_label.configure(text=f"Author: {task['author']}")
        self.task_description.configure(text=task["description"])
        self.status_label.configure(text=f"Status: {task['status']}")
        self.deadline_label.configure(text=f"Deadline: {task['deadline']}")
        self.created_at_label.configure(text=f"Created At: {task['createdAt']}")
        
        # Форматируем теги как строку
        tags = ", ".join(task["tags"])
        self.tags_label.configure(text=f"Tags: {tags}")
