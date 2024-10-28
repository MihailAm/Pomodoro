from redis import asyncio as redis

from settings import Settings


def get_redis_connection() -> redis.Redis:
    setting = Settings()
    return redis.Redis(
        host=setting.CACHE_HOST,
        port=setting.CACHE_PORT,
        db=setting.CACHE_DB,
    )
