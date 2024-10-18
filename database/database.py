from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import Settings

settings = Settings()
engine = create_engine(settings.db_url)

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session

Base = declarative_base()