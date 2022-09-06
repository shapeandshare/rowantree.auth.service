""" The Rowan Tree Service Layer Handler(s) """

import logging
import os
from pathlib import Path

from fastapi import FastAPI, status
from mysql.connector.pooling import MySQLConnectionPool
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from ..config.server import ServerConfig
from ..db.dao import DBDAO
from ..db.utils import get_connect_pool

# Generating server configuration
config: ServerConfig = ServerConfig()

# Setup logging
Path(config.log_dir).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
    filemode="w",
    filename=f"{config.log_dir}/{os.uname()[1]}.therowantree.service.log",
)

logging.debug("Starting server")

logging.debug(config.json(by_alias=True, exclude_unset=True))

# Creating database connection pool, and DAO
cnxpool: MySQLConnectionPool = get_connect_pool(config=config)
dao: DBDAO = DBDAO(cnxpool=cnxpool)

# Create controllers

# Create the FastAPI application
app = FastAPI()

#  Apply COR Configuration | https://fastapi.tiangolo.com/tutorial/cors/
origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Naive auth system until idp can be introduced
def authorize(api_access_key: str) -> None:
    """
    Performs naive authorization.

    Parameters
    ----------
    api_access_key: str
        The external provided access key to validate.
    """

    if api_access_key != config.access_key:
        logging.debug("bad access key")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad Access Key")


# Define our handlers


@app.get("/health/plain", status_code=status.HTTP_200_OK)
async def health_plain() -> bool:
    """
    Get Application Health
    [GET] /health/plain

    Returns
    -------
    [STATUS CODE] 200: OK
        health: bool
            A true/false response of server health.
    """

    return True
