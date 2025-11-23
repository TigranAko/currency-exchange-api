from fastapi import APIRouter, Depends, HTTPException, Response, status

# from fastapi.security.http import HTTPBasicCredentials
from app.api.schemas.user import UserCreds, UserInDB, UserResponse
from app.core.security import (
    create_cookie_auth,
    create_jwt_acces_token,
    create_password_hash,
    get_username,
    security,
    verify_password_hash,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


u = UserInDB(username="test", hashed_password=create_password_hash("password"))

fake_db: dict[str, str] = {u.username: u.hashed_password}
print(fake_db)


@router.post("/register", response_model=UserResponse)
async def register(creds: UserCreds = Depends()):
    # Нужно добавить проверку на существование в БД
    password_hash = create_password_hash(creds.password)
    user = UserInDB(username=creds.username, hashed_password=password_hash)
    fake_db[user.username] = password_hash
    return {
        "ok": True,
        "message": "Вы зарегестрированы",
        "data": {
            # user.model_dump()
            "username": creds.username
        },
    }


@router.post("/login")
async def login(response: Response, creds: UserCreds = Depends()):
    if creds.username not in fake_db or not verify_password_hash(
        creds.password, fake_db[creds.username]
    ):
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
