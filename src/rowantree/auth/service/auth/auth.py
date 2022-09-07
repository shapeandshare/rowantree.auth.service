import logging
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException

from ..contracts.dto.token import Token
from ..contracts.dto.token_data import TokenData
from ..contracts.dto.user_in_db import UserInDB
from ..db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_service import AbstractService


class AuthService(AbstractService):
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user: Optional[UserInDB] = None

        try:
            user = self.dao.get_user_from_db_by_username(username=username)
        except IncorrectRowCountError as error:
            logging.debug(f"User not found: {str(error)}")

        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    def create_user_access_token(self, user: UserInDB) -> Token:
        data: dict = {"sub": user.guid, "disabled": user.disabled, "admin": user.admin}
        return self.create_access_token(data=data)

    def create_access_token(self, data: dict) -> Token:
        to_encode: dict = data.copy()
        expire: datetime = datetime.utcnow() + timedelta(minutes=self.config.expiration_time)
        to_encode.update({"iss": self.config.issuer, "exp": expire})  # TODO: use fully qualified domain name
        encoded_jwt: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return Token(access_token=encoded_jwt, token_type="bearer")

    def get_user_by_jwt(self, token: str) -> UserInDB:
        credentials_exception: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = jwt.decode(
                token, self.config.secret_key, algorithms=[self.config.algorithm], issuer=self.config.issuer
            )
            guid: Optional[str] = payload.get("sub")
            if guid is None:
                raise credentials_exception
            token_data: TokenData = TokenData(guid=guid)
        except JWTError:
            raise credentials_exception

        user: Optional[UserInDB] = None

        try:
            user = self.dao.get_user_from_db_by_guid(guid=token_data.guid)
        except IncorrectRowCountError as error:
            logging.debug(f"User not found: {str(error)}")

        if user is None:
            raise credentials_exception

        return user
