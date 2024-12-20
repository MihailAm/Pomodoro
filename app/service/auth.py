from dataclasses import dataclass
import datetime as dt
from datetime import timedelta
from jose import jwt, JWTError

from app.client import GoogleClient
from app.client import YandexClient
from app.exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from app.repository import UserRepository
from app.schema import UserLoginSchema, UserCreateSchema
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (dt.datetime.now() + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expire_date_unix},
                           self.settings.JWT_SECRET_KEY,
                           algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token,
                                 key=self.settings.JWT_SECRET_KEY,
                                 algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect

        if payload['expire'] < dt.datetime.now().timestamp():
            raise TokenExpired

        return payload['user_id']

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code=code)
        user = await self.user_repository.get_user_by_email(email=user_data.email)
        if user:
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(google_access_token=user_data.access_token,
                                            email=user_data.email,
                                            name=user_data.name)
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)

        user = await self.user_repository.get_user_by_email(email=user_data.default_email)
        if user:
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
            )

        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
