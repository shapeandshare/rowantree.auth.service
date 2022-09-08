""" Auth Service User Base Definition """

from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Auth Service User Base

    Attributes
    ----------
    username: str
        The username of the user.
    guid: str
        The user guid.
    email: Union[str, None] = None
        The user email address.
    disabled: Union[bool, None] = None
        Whether the account is enabled or not.
    admin: Union[bool, None] = None
        Whether the account is an admin or not.
    """

    username: str
    guid: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None
    admin: Union[bool, None] = None
