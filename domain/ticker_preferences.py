import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from domain.audit import Audit
from domain.base import Base  # Importas la base común

class TickerPreferences(Base, Audit):
    __tablename__ = 'ticker_preferences'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String, nullable=False)
    drop_percentage = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="ticker_preferences")

    def __init__(self, ticker=None, drop_percentage=None, days=None, user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.ticker = ticker
        self.drop_percentage = drop_percentage
        self.days = days
        self.user_id = user_id
