""" Abstract Controller Definition """

from abc import abstractmethod
from typing import Any, Optional

from rowantree.contracts import BaseModel

from ..services.auth import AuthService


class AbstractController(BaseModel):
    """
    Abstract Controller

    Attributes
    ----------
    auth_service: AuthService
        The Auth Service.
    """

    auth_service: AuthService

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Should be implemented in the subclass"""
