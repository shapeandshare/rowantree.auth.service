from typing import Any, Optional

from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

from ..contracts.dto.user_in_db import UserInDB
from .abstract_controller import AbstractController


class TokenController(AbstractController):
    def execute(self, request: OAuth2PasswordRequestForm) -> Optional[Any]:
        user_dict = self.auth_service.fake_users_db.get(request.username)

        if not user_dict:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        user = UserInDB(**user_dict)
        hashed_password = self.auth_service.fake_hash_password(request.password)

        if not hashed_password == user.hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        return {"access_token": user.username, "token_type": "bearer"}
