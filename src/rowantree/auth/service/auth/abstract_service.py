""" Abstract Controller Definition """

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..db.dao import DBDAO


class AbstractService(ABC):
    """
    Abstract Service

    Attributes
    ----------
    dao: DBDAO
        The database DAO.
    """

    dao: DBDAO

    def __init__(self, dao: DBDAO):
        self.dao = dao
