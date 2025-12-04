from fastapi import APIRouter, Depends

from app.api.schemas.user import UserCreds, UserInDB
from app.core.security import security
from app.services.user_service import UserService, get_user, get_user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
    creds: UserCreds = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.register(creds=creds)


@router.post("/login")
async def login(
    creds: UserCreds = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.login(creds=creds)


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"ok": True, "message": "You Authorized"}


@router.get("/me")
async def me(user: UserInDB = Depends(get_user)):
    return {
        "ok": True,
        "message": "Вы зарегестрированный пользователь",
        "data": {"username": user},
    }


@router.get("/logout")
async def logout(user_service: UserService = Depends(get_user_service)):
    return user_service.logout()
