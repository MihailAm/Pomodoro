from fastapi import Depends

from cache import get_redis_connection
from database import get_db_session
from repository import TaskRepository, TaskCache
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_task_cache_repository() -> TaskCache:
    redis = get_redis_connection()
    return TaskCache(redis)


def get_task_service(task_repository: TaskRepository = Depends(get_tasks_repository),
                     task_cache: TaskCache = Depends(get_task_cache_repository)) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)
