from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException

from ..contracts.dto.token import Token
from ..contracts.dto.user_in_db import UserInDB
from .abstract_controller import AbstractController


class TokenController(AbstractController):
    def execute(self, request: OAuth2PasswordRequestForm) -> Token:
        user: Optional[UserInDB] = self.auth_service.authenticate_user(request.username, request.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return self.auth_service.create_user_access_token(user=user)
