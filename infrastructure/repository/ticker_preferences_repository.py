from sqlalchemy.orm import Session
from domain.ticker_preferences import TickerPreferences
from infrastructure.database.connection import get_session


class TickerPreferencesRepository:
    def __init__(self, session: Session = None):
        self.session = session or get_session()

    def get_by_user_id(self, user_id: str):
        return self.session.query(TickerPreferences).filter(
            TickerPreferences.user_id == user_id
        ).all()

    def get_by_ticker(self, ticker: str):
        return self.session.query(TickerPreferences).filter(
            TickerPreferences.ticker == ticker
        ).all()

    def get_all(self):
        return self.session.query(TickerPreferences).all()

    def create(self, ticker, drop_percentage, days, user_id):
        pref = TickerPreferences(
            ticker=ticker,
            drop_percentage=drop_percentage,
            days=days,
            user_id=user_id
        )
        self.session.add(pref)
        self.session.commit()
        self.session.refresh(pref)
        return pref

    def update(self, pref_id, **kwargs):
        pref = self.session.query(TickerPreferences).filter(
            TickerPreferences.id == pref_id
        ).first()
        if not pref:
            return None
        for key, value in kwargs.items():
            if hasattr(pref, key):
                setattr(pref, key, value)
        self.session.commit()
        self.session.refresh(pref)
        return pref

    def delete(self, pref_id):
        pref = self.session.query(TickerPreferences).filter(
            TickerPreferences.id == pref_id
        ).first()
        if not pref:
            return False
        self.session.delete(pref)
        self.session.commit()
        return True
