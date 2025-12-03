import requests
import os
from dotenv import load_dotenv


class TickerSearch:
    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))
        self.api_key = os.getenv("API_KEY_ALPHA_VANTAGE")
        self.base_url = os.getenv("URL_ALPHA_VANTAGE")

    def get_ticker(self, query: str) -> dict:
        """
        Busca tickers que coincidan con la consulta dada utilizando la API de Alpha Vantage.
        """
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": query,
            "apikey": self.api_key
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        matches = data.get("bestMatches", [])
        tickers = [
            {
                "symbol": match.get("1. symbol", ""),
                "name": match.get("2. name", "")
            }
            for match in matches
        ]

        return {
            "query": query,
            "tickers": tickers
        }
