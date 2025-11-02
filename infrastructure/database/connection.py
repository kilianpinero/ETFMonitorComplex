from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.base import Base
import os
from dotenv import load_dotenv
from domain.user import User
from domain.ticker_preferences import TickerPreferences

ENV = '.env.local'

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env.local'))
load_dotenv(dotenv_path)

engine = None
Session = None


def get_engine():
    global engine
    if engine is None:
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')

        # Verifica que las variables necesarias existan
        if not all([db_user, db_pass, db_name]):
            raise ValueError("Faltan variables de entorno: DB_USER, DB_PASS o DB_NAME")

        db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_url, echo=True)

        # Crea las tablas automáticamente si no existen
        Base.metadata.create_all(engine)
    return engine


def get_session():
    global Session
    if Session is None:
        Session = sessionmaker(bind=get_engine())
    return Session()