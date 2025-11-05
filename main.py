from application.stock_drop_analyzer import StockDropAnalyzer
from application.user_preferences_analyzer_service import UserPreferencesAnalyzerService
from application.email_notifier import EmailNotifier
from fastapi import FastAPI
from infrastructure.api.ticker_preferences_controller import router as preferences_router
from infrastructure.api.login import router as login_router
from infrastructure.api.ticker_search_controller import router as ticker_router
from apscheduler.schedulers.background import BackgroundScheduler


# analyzer = StockDropAnalyzer()
# drop = analyzer.get_drop_percentage("NA9.DE", 90, 10)
# print(f"📉  ha caído un {drop.get('drop_percentage')}% en los últimos {drop.get('days_ago')} días")


# results = [
#     {
#         "ticker": "GOOGL",
#         "drop_percentage": -0.67,
#         "highest_price": 269.27,
#         "current_price": 267.47,
#         "alert": True,
#         "days_ago": 45
#     },
#     {
#         "ticker": "MSFT",
#         "drop_percentage": 0.0,
#         "highest_price": 542.07,
#         "current_price": 542.07,
#         "alert": True,
#         "days_ago": 15
#     },
#     {
#         "ticker": "TSLA",
#         "drop_percentage": 0.0,
#         "highest_price": 460.55,
#         "current_price": 460.55,
#         "alert": True,
#         "days_ago": 60
#     }
# ]
#
# service = UserPreferencesAnalyzerService()
# notifier = EmailNotifier()
# # results = service.analyze_user_tickers("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
# for result in results:
#     if result.get('alert', False):
#         print(f"🚨 Alerta de caída para {result.get('ticker')}: {result.get('drop_percentage')}%")
#
# notifier.send_email("kilianpinero@gmail.com", results)

app = FastAPI()
service = UserPreferencesAnalyzerService()

# Registrar el controlador de preferencias
def include_routers():
    app.include_router(preferences_router)
    app.include_router(login_router)
    app.include_router(ticker_router)

# arrancar scheduler
def scheduler_starter():
    scheduler = BackgroundScheduler()
    scheduler.add_job(service.check_all_tickers, 'cron', hour='12,18', minute=0, timezone='Europe/Madrid')
    scheduler.start()


include_routers()
scheduler_starter()