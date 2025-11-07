from infrastructure.repository.ticker_preferences_repository import TickerPreferencesRepository
from application.stock_drop_analyzer import StockDropAnalyzer
from infrastructure.repository.user_repository import UserRepository
from application.email_notifier import EmailNotifier
import threading

def prepare_email_report(results):
    return [result for result in results if result.get('alert', False)]

class UserPreferencesAnalyzerService:
    def __init__(self):
        self.ticker_pref_repo = TickerPreferencesRepository()
        self.analyzer = StockDropAnalyzer()

    def check_all_tickers(self):
        email_service = EmailNotifier()
        user_repo = UserRepository()
        users = user_repo.get_all_users()
        for user in users:
            results = self.analyze_user_tickers(user.id)
            report = prepare_email_report(results)
            # using Threads to send emails concurrently
            # threading.Thread(target=email_service.send_email, args=(user.email, report)).start()
            threading.Thread(target=print, args=(f"Email to: {user.email}, Report: {report}",)).start()

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