from api.base import BaseAPIClient

class UserAPIClient(BaseAPIClient):
    def create_user(self, user_data):
        return self.post("auth/signup", user_data)
    
    def login(self, email: str, password: str):
        url = "auth/signin"
        data = {"email": email, "password": password}

        response = self.post(url, data)

        print(f"Login response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers["Authorization"] = f"Bearer {self.token}"
            print(f"Token set in UserAPIClient: {self.token}")  # Отладка
        return response
        
    def user_info(self):
        url = "users/me"
        response = self.get(url)
        return response
        
    def get_token(self):
        print(f"Returning token: {self.token}")
        return self.token
        
