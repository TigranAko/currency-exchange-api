from authx import AuthX, AuthXConfig
from fastapi import Response
from passlib.context import CryptContext

from .config import ConfigAuth

pwd_context = CryptContext(
    schemes=["bcrypt"]  # нужно изменить bcrypt на argon2 (или обновить bcrypt)
)


def create_password_hash(password: str) -> str:
    password = password.encode("utf-8")
    return pwd_context.hash(password)


def verify_password_hash(password: str, hashed_password: str) -> bool:
    password = password.encode("utf-8")
    if pwd_context.verify(password, hashed_password):
        return True
    return False


config_env = ConfigAuth()

config = AuthXConfig()
config.JWT_SECRET_KEY = config_env.JWT_SECRET_KEY.get_secret_value()
config.JWT_ALGORITHM = "HS256"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

# security = OAuth2PasswordBearer(tokenUrl="/auth/login", )


def create_cookie_auth(token, response: Response):
    print(token)
    security.set_access_cookies(token=token, response=response)


def create_jwt_acces_token(username: str):
    token = security.create_access_token(uid=username)
    print(token)
    return token


# Нужно добавить refresh tokens
