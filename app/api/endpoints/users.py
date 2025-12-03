from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.schemas.user import UserCreds, UserInDB, UserResponse
from app.core.security import (
    create_cookie_auth,
    create_jwt_acces_token,
    create_password_hash,
    get_username,
    security,
    verify_password_hash,
)
from app.dependencies.database import get_session
from app.repositiries.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(
    creds: UserCreds = Depends(),
    session=Depends(get_session),
):
    # TODO: use service
    urepo = UserRepository(session)
    if urepo.get_by_name(creds.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким именем уже существует",
        )

    password_hash = create_password_hash(creds.password)
    creds = creds.model_dump()
    creds["password"] = password_hash
    user = urepo.create(creds)
    print("created user with id", user)
    return {
        "ok": True,
        "message": "Вы зарегестрированы",
        "data": {
            # user.model_dump()
            "username": creds["username"]
        },
    }


@router.post("/login")
async def login(
    response: Response, creds: UserCreds = Depends(), session=Depends(get_session)
):
    # TODO: use service
    urepo = UserRepository(session)
    user = urepo.get_by_name(creds.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user: UserInDB = UserInDB.model_validate(user)

    if not verify_password_hash(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_jwt_acces_token(creds.username)
    create_cookie_auth(access_token, response)
    return {
        "ok": True,
        "message": "Access token в cookie успешно создан",
        "data": {"username": creds.username, "access_token": access_token},
    }


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"ok": True, "message": "You Authorized"}


@router.get("/me")
async def me(username=Depends(get_username)):
    return {
        "ok": True,
        "message": "Вы зарегестрированный пользователь",
        "data": {"username": username},
    }


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token_cookie")
    # Возможно нужно удалять из security

    return {"ok": True, "message": "Вы успешно вышли из системы"}
