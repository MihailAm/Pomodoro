from dataclasses import dataclass
import datetime as dt
from datetime import timedelta
from jose import jwt, JWTError

from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from repository import UserRepository
from schema import UserLoginSchema
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
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
