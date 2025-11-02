import requests
import os
from dotenv import load_dotenv

class StockDropAnalyzer:
    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))
        self.api_key = os.getenv("API_KEY_ALPHA_VANTAGE")
        self.base_url = os.getenv("URL_ALPHA_VANTAGE")

    def get_drop_percentage(self, ticker: str, days_ago: int, percentage: int) -> dict:
        """
        Calcula el porcentaje de caída de una acción desde hoy hasta X días atrás:
        - Obtiene los últimos X días de datos.
        - Calcula el precio máximo de los últimos X días de cierre.
        - Compara ese máximo con el precio actual (último disponible).
        - Devuelve el porcentaje de variación: negativo si ha caído, 0 si está en maximos.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": "compact"
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        time_series = data.get("Time Series (Daily)")
        if not time_series:
            raise ValueError(f"No se encontraron datos para el ticker '{ticker}'")

        # Ordenar fechas de más reciente a más antigua
        dates = sorted(time_series.keys(), reverse=True)

        # Tomar los últimos X días de cierre
        close_prices = [float(time_series[date]["4. close"]) for date in dates[:days_ago]]
        if len(close_prices) < 2:
            raise ValueError("No hay suficientes datos para calcular la variación")

        highest_price = max(close_prices)
        current_price = close_prices[0]

        drop_percentage = ((current_price - highest_price) / highest_price) * 100

        return {
            "ticker": ticker,
            "drop_percentage": round(drop_percentage, 2),
            "highest_price": highest_price,
            "current_price": current_price,
            "alert": drop_percentage <= -percentage,  # caída
            "days_ago": days_ago
        }
