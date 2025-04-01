import os
import requests
from config import BASE_URL
BASE_URL = os.getenv("BASE_URL")

class BaseAPIClient:
    def __init__(self, token: str = None): 
        self.token = None
        self.base_url = BASE_URL
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def get(self, endpoint: str):
        response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
        return response

    def post(self, endpoint: str, data: str):
        response = requests.post(
            f"{self.base_url}/{endpoint}", 
            json=data, 
            headers=self.headers
        )
        return response

