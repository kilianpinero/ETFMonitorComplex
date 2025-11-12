from infrastructure.database.connection import get_engine
from domain.base import Base
from domain.user import User
from domain.subscription import Subscription
from domain.ticker_preferences import TickerPreferences

engine = get_engine()
Base.metadata.create_all(engine)
print("Tablas creadas o verificadas exitosamente")