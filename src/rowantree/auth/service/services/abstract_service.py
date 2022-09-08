""" Abstract Controller Definition """

from pydantic import BaseModel

from .db.dao import DBDAO


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
        """
        Pydantic Default Configuration Over-Ride
        """

        arbitrary_types_allowed = True
