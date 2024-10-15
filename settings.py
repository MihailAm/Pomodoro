from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = '1234'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
