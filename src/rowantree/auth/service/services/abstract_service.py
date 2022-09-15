""" Abstract Controller Definition """

from rowantree.contracts import BaseModel

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
