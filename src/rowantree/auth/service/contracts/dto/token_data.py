from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    guid: Union[str, None] = None
