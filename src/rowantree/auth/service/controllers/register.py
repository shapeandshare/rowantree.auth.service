""" Register Controller Definition """
from typing import Optional

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.auth.sdk import RegisterUserRequest, User, UserBase

from .abstract_controller import AbstractController


class RegisterController(AbstractController):
    """Register Controller"""

    def execute(self, request: RegisterUserRequest) -> UserBase:
        """
        Create new user.

        Parameters
        ----------
        request: RegisterUserRequest
            Form data for new user creation.
        """

        user: Optional[User] = self.auth_service.register_user(request=request)

        if not user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unable to create user")

        return UserBase.parse_obj(user)
