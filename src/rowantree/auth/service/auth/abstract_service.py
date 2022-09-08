""" Abstract Controller Definition """

from pydantic import BaseModel

from ..db.dao import DBDAO


class AbstractService(BaseModel):
    """
    Abstract Service

    Attributes
    ----------
    dao: DBDAO
        The database DAO.
    """

    dao: DBDAO

    class Config:
        arbitrary_types_allowed = True
