from sqlalchemy.orm import Session
from domain.user import User
from infrastructure.database.connection import get_session


class UserRepository:
    def __init__(self, session: Session = None):
        self.session = session or get_session()

    def get_by_id(self, user_id: str):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_with_preferences(self, user_id: str):
        return self.session.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, email: str, password: str):
        new_user = User(username=username, email=email, password=password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user