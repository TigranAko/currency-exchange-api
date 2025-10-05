from authx import AuthX, AuthXConfig, TokenPayload
from uuid import UUID
from fastapi import Response, Depends
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET_KEY = "5adb6490e8f0ba43b9394842f7fdf329ff5df2b2142a0c3f39b6f531e1112ee3"

config = AuthXConfig()
config.JWT_SECRET_KEY = JWT_SECRET_KEY
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
