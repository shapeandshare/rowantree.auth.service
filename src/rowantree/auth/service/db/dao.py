""" Database DAO Definition """

import logging
import socket
from typing import Optional, Tuple

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool


class DBDAO:
    """
    Database DAO

    Attributes
    ----------
    cnxpool: Any
        MySQL Connection Pool
    """

    cnxpool: MySQLConnectionPool

    def __init__(self, cnxpool: MySQLConnectionPool):
        self.cnxpool = cnxpool

    # pylint: disable=duplicate-code
    def _call_proc(self, name: str, args: list, debug: bool = False) -> Optional[list[Tuple]]:
        """
        Perform a stored procedure call.

        Parameters
        ----------
        name: str
            The name of the stored procedure to call.
        args: list
            The arguments to pass to the stored procedure.
        debug: bool
            Whether to log debug details about the call.

        Returns
        -------
        results: Optional[list[Tuple]]
            An optional list of tuples (rows) from the call.
        """

        if debug:
            logging.debug("[DAO] [Stored Proc Call Details] Name: {%s}, Arguments: {%s}", name, args)
        rows: Optional[list[Tuple]] = None
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.callproc(name, args)
            for result in cursor.stored_results():
                rows = result.fetchall()
            cursor.close()
        except socket.error as error:
            logging.debug(error)
            raise error
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.debug("Something is wrong with your user name or password")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                logging.debug("Database does not exist")
            else:
                logging.debug(error)
            raise error
        else:
            cnx.close()

        if debug:
            logging.debug("[DAO] [Stored Proc Call Details] Returning:")
            logging.debug(rows)
        return rows
