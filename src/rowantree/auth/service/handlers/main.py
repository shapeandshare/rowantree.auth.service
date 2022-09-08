""" The Rowan Tree Auth Service Definition """

import logging
import os
from pathlib import Path

from fastapi import Depends, FastAPI, status
from fastapi.security import OAuth2PasswordRequestForm
from mysql.connector.pooling import MySQLConnectionPool
from starlette.middleware.cors import CORSMiddleware

from rowantree.auth.sdk.contracts.dto.token import Token
from rowantree.common.sdk import demand_env_var

from ..controllers.token import TokenController
from ..services.auth import AuthService
from ..services.db.dao import DBDAO
from ..services.db.utils import get_connect_pool

# Setup logging
Path(demand_env_var(name="LOGS_DIR")).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
    filemode="w",
    filename=f"{demand_env_var(name='LOGS_DIR')}/{os.uname()[1]}.therowantree.auth.service.log",
)

logging.debug("Starting server")

# Creating database connection pool, and DAO
cnxpool: MySQLConnectionPool = get_connect_pool()
dao: DBDAO = DBDAO(cnxpool=cnxpool)
auth_service: AuthService = AuthService(dao=dao)


# Create controllers
token_controller: TokenController = TokenController(auth_service=auth_service)

# Create the FastAPI application
app = FastAPI()

#  Apply COR Configuration | https://fastapi.tiangolo.com/tutorial/cors/
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define our handlers


@app.get("/health/plain", status_code=status.HTTP_200_OK)
def health_plain() -> bool:
    """
    Get Application Health
    [GET] /health/plain

    Returns
    -------
    health: bool
        A true/false response of server health.

    [STATUS CODE] 200: OK
    [STATUS CODE] 400: Invalid Request
    [STATUS CODE] 500: Internal Server Error
    """

    return True


@app.post("/v1/auth/token", status_code=status.HTTP_200_OK)
def token_handler(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Get Token
    [POST] /v1/auth/token

    Returns
    -------
    token: Token

    [STATUS CODE] 200: OK
    [STATUS CODE] 400: Invalid Request
    [STATUS CODE] 401: Permission Denied
    [STATUS CODE] 500: Internal Server Error
    """

    return token_controller.execute(request=form_data)
