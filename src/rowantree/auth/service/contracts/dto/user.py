from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    username: str
    guid: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None
    admin: Union[bool, None] = None
