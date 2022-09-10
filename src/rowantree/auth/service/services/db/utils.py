""" DB DAO Utilities """

import logging
import socket
import time
from typing import Optional

from mysql.connector import Error, errorcode
from mysql.connector.pooling import MySQLConnectionPool

from rowantree.common.sdk import demand_env_var


# pylint: disable=duplicate-code
def get_connect_pool() -> MySQLConnectionPool:
    """
    Gets a connection pool to the database.

    Returns
    -------
    cnxpool: MySQLConnectionPool
        A connection pool to the database server.
    """

    try:
        logging.debug("Connecting to database")
        cnxpool: MySQLConnectionPool = MySQLConnectionPool(
            pool_name="servercnxpool",
            pool_size=3,
            user=demand_env_var(name="DATABASE_USERNAME"),
            password=demand_env_var(name="DATABASE_PASSWORD"),
            host=demand_env_var(name="DATABASE_SERVER"),
            database=demand_env_var(name="DATABASE_NAME"),
        )
        return cnxpool
    except socket.error as error:
        logging.debug(str(error))
        raise error from error
    except Error as error:
        logging.debug(str(error))
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.debug("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            logging.debug("Database does not exist")
        raise error from error
    except Exception as error:
        logging.debug(str(error))
        raise error from error


class WrappedConnectionPool:
    """
    Manages the creation of a MySQL connection pool along with reties.

    Attributes
    ----------
    retry_wait: int = 1
        The number of seconds to wait between attempts.
    healthy: bool = False
        Whether a pool was created.
    cnxpool: Optional[MySQLConnectionPool] = None
        The created connection pool.
    """

    retry_wait: int = 1
    healthy: bool = False
    cnxpool: Optional[MySQLConnectionPool] = None

    def __init__(self):
        # Attempts forever.  In the expected consumption scenario we would want this to occur indefinitely.
        while not self.healthy:
            self.healthy = self.connect()

    def connect(self) -> bool:
        """
        Attempts to create a database connection pool.

        Returns
        -------
        result: bool
            True or False depending on whether a pool was successfully created.
        """

        # pylint: disable=broad-except
        try:
            self.cnxpool = get_connect_pool()
            return True
        except Exception as error:
            logging.error("Unable to create connection pool, retrying ..")
            logging.error(str(error))
            time.sleep(self.retry_wait)
            return False
