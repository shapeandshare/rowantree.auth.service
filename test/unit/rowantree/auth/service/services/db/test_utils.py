import os
import unittest
from unittest.mock import call, patch


class TestUtils(unittest.TestCase):
    def test_get_connect_pool(self):

        with patch("mysql.connector.pooling.MySQLConnectionPool") as mock_cnxpool:
            from src.rowantree.auth.service.services.db.utils import get_connect_pool

            get_connect_pool()

        self.assertTrue(mock_cnxpool.call_count == 1)
        print(mock_cnxpool.mock_calls)
        self.assertEqual(
            mock_cnxpool.mock_calls[0],
            call(
                pool_name="servercnxpool",
                pool_size=3,
                user=os.environ["DATABASE_USERNAME"],
                password=os.environ["DATABASE_PASSWORD"],
                host=os.environ["DATABASE_SERVER"],
                database=os.environ["DATABASE_NAME"],
            ),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(TestUtils())
