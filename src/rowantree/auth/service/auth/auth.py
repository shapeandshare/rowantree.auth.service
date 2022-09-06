from fastapi.security import OAuth2PasswordBearer

from ..contracts.dto.user_in_db import UserInDB
from .abstract_service import AbstractService


class AuthService(AbstractService):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "fakehashedsecret",
            "disabled": False,
        },
        "alice": {
            "username": "alice",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "hashed_password": "fakehashedsecret2",
            "disabled": True,
        },
    }

    def get_user(self, db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    def fake_decode_token(self, token):
        # This doesn't provide any security at all
        # Check the next version
        user = self.get_user(self.fake_users_db, token)
        return user

    def fake_hash_password(self, password: str):
        return "fakehashed" + password
