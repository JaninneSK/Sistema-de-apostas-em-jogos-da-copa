import os
import requests
from dotenv import load_dotenv


load_dotenv()

class APIClient:

    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):
        self.token = os.getenv("FOOTBALL_DATA_TOKEN")

        if not self.token:
            raise ValueError("Token da football-data.org não encontrado.")

        self.headers = {
            "X-Auth-Token": self.token
        }

    def get(self, endpoint: str, params: dict | None = None) -> dict:

        url = f"{self.BASE_URL}/{endpoint}"

        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )

        if response.status_code == 429:
            raise RuntimeError("Limite de requisições da API excedido.")

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro ao acessar a API. Status: {response.status_code}"
            )

        return response.json()