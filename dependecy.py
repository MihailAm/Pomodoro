from fastapi import Depends

from cache import get_redis_connection
from database import get_db_session
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService
from service.auth import AuthService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_task_cache_repository() -> TaskCache:
    redis = get_redis_connection()
    return TaskCache(redis)


def get_task_service(task_repository: TaskRepository = Depends(get_tasks_repository),
                     task_cache: TaskCache = Depends(get_task_cache_repository)) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)

def get_user_repository() -> UserRepository:
    db_session = get_db_session()
    return UserRepository(db_session)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)

def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository)
