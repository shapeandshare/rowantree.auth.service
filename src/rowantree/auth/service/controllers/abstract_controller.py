""" Abstract Controller Definition """

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..services.auth import AuthService


class AbstractController(ABC):
    """
    Abstract Controller

    Attributes
    ----------
    auth_service: AuthService
        The Auth Service.
    """

    auth_service: AuthService

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Should be implemented in the subclass"""
