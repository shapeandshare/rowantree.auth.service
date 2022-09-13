""" Authentication and Authorization Service Definition """

import logging
from typing import Optional

from rowantree.auth.sdk import RegisterUserRequest, User, get_password_hash, verify_password

from .abstract_service import AbstractService
from .db.incorrect_row_count_error import IncorrectRowCountError


class AuthService(AbstractService):
    """
    Authentication and Authorization Service
    """

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

        try:
            user: Optional[User] = self.dao.get_user(username=username)
        except IncorrectRowCountError as error:
            logging.debug("User not found: %s", str(error))
            return None

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user

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

    def register_user(self, request: RegisterUserRequest) -> Optional[User]:
        """
        Creates a user record in the database.

        Parameters
        ----------
        request: RegisterUserRequest
            The user registration request.

        Returns
        -------
        user: Optional[User]
            A user if one could be created, `None` otherwise.
        """

        user: User = User(
            username=request.username,
            hashed_password=get_password_hash(request.password),
            email=request.email,
            disabled=False,
            admin=False,
        )

        try:
            return self.dao.create_user(user=user)
        except IncorrectRowCountError as error:
            logging.debug("Unable to create user, possibly already exists: %s", str(error))
            return None
