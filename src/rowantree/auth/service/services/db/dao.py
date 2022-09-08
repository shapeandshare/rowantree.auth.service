""" Database DAO Definition """

import logging
import socket
from typing import Optional, Tuple

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool
from starlette import status
from starlette.exceptions import HTTPException

from ...contracts.dto.user.user import User
from .incorrect_row_count_error import IncorrectRowCountError


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

    def get_user(self, username: Optional[str] = None, guid: Optional[str] = None) -> User:
        """
        Get User (From Database) Using `username` first, else `guid`.  At least one must be supplied.

        Parameters
        ----------
        username: Optional[str]
            username
        guid: Optional[str]
            user guid

        Returns
        -------
        user: User
            User (from database)
        """

        if username is None and guid is None:
            logging.debug("get_user called without username or a guid, one is required")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        args: list[str] = [username]
        proc_name: str = "getUserByUsername"

        if username is None:
            args = [guid]
            proc_name: str = "getUserByGUID"

        rows: list[Tuple] = self._call_proc(proc_name, args, True)
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")
        user: tuple = rows[0]

        is_disabled: bool = True
        if user[6] == 0:
            is_disabled = False

        is_admin: bool = False
        if user[7] == 1:
            is_admin = True

        return User(
            username=user[2], guid=user[1], email=user[3], hashed_password=user[4], disabled=is_disabled, admin=is_admin
        )
