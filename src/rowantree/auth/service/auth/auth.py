from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException

from ..contracts.dto.token_data import TokenData
from ..contracts.dto.user import User
from ..contracts.dto.user_in_db import UserInDB
from .abstract_service import AbstractService

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService(AbstractService):
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    fake_users_db: dict = {
        "johndoe": {
            "guid": "a04ede08-f10c-4cd9-80a8-137d7081cf12",
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
            "admin": True,
        }
    }

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return self.pwd_context.hash(password)

    def get_user_from_db(self, username: str) -> Optional[UserInDB]:
        if username in self.fake_users_db:
            user_dict = self.fake_users_db[username]
            return UserInDB.parse_obj(user_dict)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user: Optional[UserInDB] = self.get_user_from_db(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        to_encode: dict = data.copy()
        if expires_delta:
            expire: datetime = datetime.utcnow() + expires_delta
        else:
            expire: datetime = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iss": "rowantree.auth.service", "exp": expire})  # TODO: use fully qualified domain name
        encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_user_from_jwt(self, token: str) -> UserInDB:
        credentials_exception: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: Optional[str] = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data: TokenData = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user: Optional[UserInDB] = self.get_user_from_db(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
