from api.base import BaseAPIClient


class TaskAPIClient(BaseAPIClient):
    def __init__(self, token=None):
        super().__init__(token)

    def create_task(self, task_data):
        return self.post("tasks", task_data)

    def get_tasks(self):
        return self.get("tasks")

    def get_tasks_by_name(self, name):
        return self.get(f"tasks?name={name}")

