""" DB DAO Utilities """

import logging
import socket

from mysql.connector import Error, errorcode
from mysql.connector.pooling import MySQLConnectionPool

from ..config.server import ServerConfig


# pylint: disable=duplicate-code
def get_connect_pool(config: ServerConfig) -> MySQLConnectionPool:
    """
    Gets a connection pool to the database.

    Parameters
    ----------
    config: ServerConfig
        The server configuration.

    Returns
    -------
    cnxpool: MySQLConnectionPool
        A connection pool to the database server.
    """

    try:
        logging.debug("Connecting to database")
        cnxpool: MySQLConnectionPool = MySQLConnectionPool(
            pool_name="servercnxpool",
            pool_size=32,
            user=config.database_username,
            password=config.database_password,
            host=config.database_server,
            database=config.database_name,
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
