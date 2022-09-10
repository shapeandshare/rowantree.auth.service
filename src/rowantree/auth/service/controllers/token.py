""" Token Controller Definition """

from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException

from rowantree.auth.sdk import Token, User, create_user_access_token

from .abstract_controller import AbstractController


class TokenController(AbstractController):
    """Token Controller"""

    def execute(self, request: OAuth2PasswordRequestForm) -> Token:
        """
        Execute the controller action. (Auth User)

        Parameters
        ----------
        request: OAuth2PasswordRequestForm
            The username/password form data

        Returns
        -------
        token: Token
            A token with the users permissions.
        """

        user: Optional[User] = self.auth_service.authenticate_user(request.username, request.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_user_access_token(user=user)
