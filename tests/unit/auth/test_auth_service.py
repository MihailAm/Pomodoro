# import pytest
import pytest
from jose import jwt
import datetime as dt

from app.schema import UserLoginSchema
from app.service import AuthService
from app.settings import Settings
from tests.fixtures.settings import settings


pytestmark = pytest.mark.asyncio


async def test_get_google_redirect_url_success(auth_service_mock: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url

    auth_service_google_redirect_url = auth_service_mock.get_google_redirect_url()

    assert settings_google_redirect_url == auth_service_google_redirect_url


async def test_get_yandex_redirect_url_success(auth_service_mock: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url
    auth_service_yandex_redirect_url = auth_service_mock.get_yandex_redirect_url()
    assert settings_yandex_redirect_url == auth_service_yandex_redirect_url


async def test_generate_access_token__success(auth_service_mock: AuthService, settings: Settings):
    user_id = 1

    access_token = auth_service_mock.generate_access_token(user_id=user_id)
    decoded_access_token = jwt.decode(access_token,
                                      settings.JWT_SECRET_KEY,
                                      algorithms=[settings.JWT_ENCODE_ALGORITHM])
    decoded_user_id = decoded_access_token.get("user_id")
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get("expire"), tz=dt.timezone.utc)

    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC)) > dt.timedelta(days=6)
    assert decoded_user_id == user_id


async def test_get_user_id_from_access_token__success(auth_service_mock: AuthService):
    user_id = 1

    access_token = auth_service_mock.generate_access_token(user_id=user_id)
    decoded_user_id = auth_service_mock.get_user_id_from_access_token(access_token=access_token)

    assert decoded_user_id == user_id


async def test_google_auth_success(auth_service_mock: AuthService):
    user = await auth_service_mock.google_auth(code="fake_code")
    decoded_user_id = auth_service_mock.get_user_id_from_access_token(access_token=user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)

async def test_yandex_auth_success(auth_service_mock: AuthService):
    user = await auth_service_mock.google_auth(code="fake_code")
    decoded_user_id = auth_service_mock.get_user_id_from_access_token(access_token=user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user , UserLoginSchema)
