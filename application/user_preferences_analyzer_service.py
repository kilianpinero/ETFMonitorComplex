from infrastructure.repository.ticker_preferences_repository import TickerPreferencesRepository
from application.stock_drop_analyzer import StockDropAnalyzer

class UserPreferencesAnalyzerService:
    def __init__(self):
        self.ticker_pref_repo = TickerPreferencesRepository()
        self.analyzer = StockDropAnalyzer()

    def analyze_user_tickers(self, user_id: str):
        results = []
        prefs = self.ticker_pref_repo.get_by_user_id(user_id)
        for pref in prefs:
            try:
                analysis = self.analyzer.get_drop_percentage(
                    ticker=pref.ticker,
                    days_ago=pref.days,
                    percentage=pref.drop_percentage
                )
                results.append(analysis)
            except Exception as e:
                results.append({"ticker": pref.ticker, "error": str(e)})
        return results