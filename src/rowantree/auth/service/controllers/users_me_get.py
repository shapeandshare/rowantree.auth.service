from ..contracts.dto.user import User
from .abstract_controller import AbstractController


class UsersMeGetController(AbstractController):
    def execute(self, request: User) -> User:
        return request
