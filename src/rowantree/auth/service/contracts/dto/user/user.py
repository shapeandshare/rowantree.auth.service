""" User Definition """

from .base import UserBase


class User(UserBase):
    """
    User Definition

    Attributes
    ----------
    hashed_password: str
        Hashed user password.
    """

    hashed_password: str
