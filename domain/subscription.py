from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import datetime
from domain.base import Base
from domain.audit import Audit

class Subscription(Base, Audit):
    __tablename__ = 'subscriptions'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    stripe_subscription_id = Column(String, nullable=True)
    start_date = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    end_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default='active')

    user = relationship("User", back_populates="subscriptions")