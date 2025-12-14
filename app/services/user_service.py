from authx import TokenPayload
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreate, UserRead
from app.core.security import (
    create_cookie_auth,
    create_jwt_acces_token,
    create_password_hash,
    security,
    verify_password_hash,
)
from app.dependencies.database import get_session
from app.repositiries.user_repository import UserRepository


class UserService:
    def __init__(self, response: Response, users_repository: UserRepository):
        self.users_repo: UserRepository = users_repository
        self.response: Response = response

    def register(self, creds: UserCreate):
        if self.users_repo.get_by_name(creds.username):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь с таким именем уже существует",
            )

        password_hash = create_password_hash(creds.password)
        creds = creds.model_dump()
        creds["password"] = password_hash
        user = self.users_repo.create(creds)
        print("created user with id", user)
        return {
            "ok": True,
            "message": "Вы зарегестрированы",
        }

    def login(self, creds: UserCreate):
        user: UserRead = self.get_user_from_db(creds.username)
        if not verify_password_hash(creds.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )

        access_token = create_jwt_acces_token(creds.username)
        create_cookie_auth(access_token, self.response)
        return {
            "ok": True,
            "message": "Access token в cookie успешно создан",
        }

    def logout(self):
        self.response.delete_cookie("access_token_cookie")
        # TODO: CHECK
        return {"ok": True, "message": "Вы успешно вышли из системы"}

    def get_user_from_db(self, username: str) -> UserRead:
        user = self.users_repo.get_by_name(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )
        user: UserRead = UserRead.model_validate(user)
        return user


# TODO: dependencies


def get_user_service(
    response: Response, session: Session = Depends(get_session)
) -> UserService:
    return UserService(response, UserRepository(session))


def get_user(
    payload: TokenPayload = Depends(security.access_token_required),
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    username: str = payload.sub
    user: UserRead = user_service.get_user_from_db(username)
    return user
