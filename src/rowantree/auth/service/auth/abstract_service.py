""" Abstract Controller Definition """

from pydantic import BaseModel

from ..config.server import ServerConfig
from ..db.dao import DBDAO


class AbstractService(BaseModel):
    """
    Abstract Service

    Attributes
    ----------
    dao: DBDAO
        The database DAO.
    config: ServerConfig
        A server config object
    """

    dao: DBDAO
    config: ServerConfig

    class Config:
        arbitrary_types_allowed = True
