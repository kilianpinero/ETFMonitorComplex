from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from domain.audit import Audit
from domain.base import Base  # Importas la base común

class User(Base, Audit):
    __tablename__ = 'users'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    ticker_preferences = relationship("TickerPreferences", back_populates="user")
