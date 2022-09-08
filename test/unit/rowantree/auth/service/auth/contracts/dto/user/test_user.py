import unittest

from src.rowantree.auth.service.contracts.dto.user.user import User


class TestUser(unittest.TestCase):
    def test_(self):
        user_dict: dict[str, str] = {
            "hashed_password": "fake_hash",
            "username": "fake_username",
            "guid": "fake_guid",
        }

        self.assertEqual(User(**user_dict).dict(exclude_unset=True), user_dict)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(TestUser())
