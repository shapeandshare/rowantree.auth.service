""" DB DAO Utilities """

import logging
import socket

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
        logging.debug(error)
        raise error
    except Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.debug("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            logging.debug("Database does not exist")
        else:
            logging.debug(error)
        raise error
