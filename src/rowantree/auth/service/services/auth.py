""" Authentication and Authorization Service Definition """

import logging
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from rowantree.auth.sdk.contracts.dto.token import Token
from rowantree.common.sdk import demand_env_var, demand_env_var_as_float

from ..contracts.dto.user.user import User
from .abstract_service import AbstractService
from .db.incorrect_row_count_error import IncorrectRowCountError


class AuthService(AbstractService):
    """
    Authentication and Authorization Service

    Attributes
    ----------
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        Password hashing context
    """

    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies hashed password.

        Parameters
        ----------
        plain_password: str
            Plan text password
        hashed_password: str
            Hashed password

        Returns
        -------
        verified: bool
            True if the password matches the hash, False otherwise.
        """

        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generates password hash.

        Parameters
        ----------
        password: str
            Plain text password.

        Returns
        -------
        hashed_password: str
            Hashed password.
        """

        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticates a user by username/password.

        Parameters
        ----------
        username: str
            Username
        password:
            Plain text password.

        Returns
        -------
        user: Optional[User]
            Returns an instance of `UserInDB` if successfully authenticated, otherwise `None`.
        """

        user: Optional[User] = None

        try:
            user = self.dao.get_user(username=username)
        except IncorrectRowCountError as error:
            logging.debug("User not found: %s", str(error))
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def create_user_access_token(user: User) -> Token:
        """
        Create bearer Token from user instance.

        Parameters
        ----------
        user: User
            An instance of a UserInDB object.

        Returns
        -------
        token: Token
            A bearer token for the requested user.
        """

        # Currently these are the claims we pull from the database.
        data: dict = {"sub": user.guid, "disabled": user.disabled, "admin": user.admin}
        return AuthService.create_access_token(data=data)

    @staticmethod
    def create_access_token(data: dict) -> Token:
        """
        Mints the access token.

        Parameters
        ----------
        data: dict
            The base set of claims to include in the token.

        Returns
        -------
        token: Token
            A newly minted token.
        """

        to_encode: dict = data.copy()
        expire: datetime = datetime.utcnow() + timedelta(
            minutes=demand_env_var_as_float(name="ACCESS_TOKEN_EXPIRATION_TIME")
        )
        to_encode.update({"iss": demand_env_var(name="ACCESS_TOKEN_ISSUER"), "exp": expire})
        encoded_jwt: str = jwt.encode(
            to_encode,
            demand_env_var(name="ACCESS_TOKEN_SECRET_KEY"),
            algorithm=demand_env_var(name="ACCESS_TOKEN_ALGORITHM"),
        )
        return Token(access_token=encoded_jwt, token_type="bearer")

    # TODO: Future functionality.
    # def get_user_by_jwt(self, token: str) -> User:
    #     credentials_exception: HTTPException = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     user: Optional[User] = None
    #     token_claims: TokenClaims = get_claims(token=token)
    #
    #     try:
    #         user = self.dao.get_user(guid=token_claims.sub)
    #     except IncorrectRowCountError as error:
    #         logging.debug(f"User not found: {str(error)}")
    #
    #     if user is None:
    #         raise credentials_exception
    #
    #     return user
