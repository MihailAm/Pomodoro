from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5433/pomodoro')

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session