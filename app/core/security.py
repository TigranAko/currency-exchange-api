from authx import AuthX, AuthXConfig, TokenPayload
from uuid import UUID
from fastapi import Response, Depends
from fastapi.security import OAuth2PasswordBearer
from .config import ConfigAuth

config_env = ConfigAuth()

config = AuthXConfig()
config.JWT_SECRET_KEY = config_env.JWT_SECRET_KEY.get_secret_value()
config.JWT_ALGORITHM = "HS256"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

#security = OAuth2PasswordBearer(tokenUrl="/auth/login", )


def create_cookie_auth(token, response: Response):
    print(token)
    security.set_access_cookies(token=token, response=response)
#    response.set_cookie('access_token_cookie', token)

def create_jwt_acces_token(username: str):
    token = security.create_access_token(uid=username)
    print(token)
    return token


def get_username(payload: TokenPayload = Depends(security.access_token_required)):
    return payload.sub
