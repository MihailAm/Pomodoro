import pytest
import pytest_asyncio

from app.repository import UserRepository
from app.service import AuthService, UserService
from app.settings import Settings


@pytest.fixture
def auth_service_mock(yandex_client, google_client, user_repository):
    return AuthService(user_repository=user_repository,
                       settings=Settings(),
                       google_client=google_client,
                       yandex_client=yandex_client)


@pytest_asyncio.fixture
def auth_service(yandex_client, google_client, auth_service_mock, get_db_session):
    return AuthService(user_repository=UserRepository(db_session=get_db_session),
                       settings=Settings(),
                       google_client=google_client,
                       yandex_client=yandex_client)

