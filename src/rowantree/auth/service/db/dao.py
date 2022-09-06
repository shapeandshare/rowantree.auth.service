""" Database DAO Definition """

import logging
import socket
from typing import Optional, Tuple

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool

from ..contracts.dto.user_in_db import UserInDB


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

    fake_users_db: dict = {
        "johndoe": {
            "guid": "a04ede08-f10c-4cd9-80a8-137d7081cf12",
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
            "admin": True,
        }
    }

    def get_user_from_db_by_username(self, username: str) -> Optional[UserInDB]:
        if username in self.fake_users_db:
            user_dict = self.fake_users_db[username]
            return UserInDB.parse_obj(user_dict)

    def get_user_from_db_by_guid(self, guid: str) -> Optional[UserInDB]:
        for user in self.fake_users_db.values():
            if guid == user["guid"]:
                return UserInDB.parse_obj(user)
