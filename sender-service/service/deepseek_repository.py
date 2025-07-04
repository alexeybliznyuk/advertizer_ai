import requests
from settings.config import settings


class DeepSeekRepository:
    def __init__(self):
        self.api_key = settings.COURSE_STRUCTURE_AI_API_KEY
        self.url = settings.COURSE_STRUCTURE_AI_REQUESTS_URL

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def call_deepseek_api(self, data):
        response = requests.post(self.url, headers=self.headers, json=data)
        print(response)
        return response.json() 