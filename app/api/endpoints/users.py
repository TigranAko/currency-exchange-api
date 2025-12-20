from fastapi import APIRouter, Depends

from app.api.schemas.user import UserCreate, UserRead, UserResponse
from app.core.security import security
from app.services.user_service import UserService, get_user, get_user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201, response_model=UserResponse)
async def register(
    creds: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return user_service.register(creds=creds)


@router.post("/login", status_code=201, response_model=UserResponse)
async def login(
    creds: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.login(creds=creds)


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"ok": True, "message": "You Authorized"}


@router.get("/me")
async def me(user: UserRead = Depends(get_user)):
    return {
        "ok": True,
        "message": "Вы зарегестрированный пользователь",
        "data": {"username": user},
    }


@router.post("/logout")
async def logout(user_service: UserService = Depends(get_user_service)):
    return user_service.logout()
