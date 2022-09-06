""" The Rowan Tree Service Layer Handler(s) """

import logging
import os
from pathlib import Path

from fastapi import Depends, FastAPI, status
from fastapi.security import OAuth2PasswordRequestForm
from mysql.connector.pooling import MySQLConnectionPool
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from ..auth.auth import AuthService
from ..config.server import ServerConfig
from ..contracts.dto.user import User
from ..controllers.token import TokenController
from ..controllers.users_me_get import UsersMeGetController
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
auth_service: AuthService = AuthService(dao=dao)


async def get_current_user(token: str = Depends(auth_service.oauth2_scheme)):
    user = auth_service.fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Create controllers
token_controller: TokenController = TokenController(auth_service=auth_service)
users_me_get_controller: UsersMeGetController = UsersMeGetController(auth_service=auth_service)

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


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return token_controller.execute(request=form_data)


@app.get("/users/me")
async def users_me_get(current_user: User = Depends(get_current_active_user)):
    return users_me_get_controller.execute(request=current_user)
