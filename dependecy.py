from fastapi import Depends, security, HTTPException
from fastapi.params import Security

from cache import get_redis_connection
from client import GoogleClient, YandexClient
from database import get_db_session
from exception import TokenExpired, TokenNotCorrect
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService
from service.auth import AuthService
from settings import Settings


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


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository),
                     google_client: GoogleClient = Depends(get_google_client),
                     yandex_client: YandexClient = Depends(get_yandex_client)) -> AuthService:
    return AuthService(user_repository=user_repository,
                       settings=Settings(),
                       google_client=google_client,
                       yandex_client=yandex_client)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository),
                     auth_service: AuthService = Depends(get_auth_service)) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(auth_service: AuthService = Depends(get_auth_service),
                        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    return user_id
