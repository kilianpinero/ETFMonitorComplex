from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from domain.audit import Audit
from domain.base import Base  # Importas la base común
from domain.subscription import Subscription

class User(Base, Audit):
    __tablename__ = 'users'

    def __init__(self, username, email, password, stripe_customer_id=None, is_premium=False):
        self.username = username
        self.email = email
        self.password = password
        self.stripe_customer_id = stripe_customer_id
        self.is_premium = is_premium

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    stripe_customer_id = Column(String, nullable=True, unique=True)
    is_premium = Column(Boolean, nullable=False, default=False)

    ticker_preferences = relationship("TickerPreferences", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
