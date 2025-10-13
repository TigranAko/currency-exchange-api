from fastapi import APIRouter, HTTPException, status, Response, Depends
#from fastapi.security.http import HTTPBasicCredentials
from app.api.schemas.user import UserCreds, UserInDB
from app.core.security import create_jwt_acces_token, create_cookie_auth, security, get_username, create_password_hash, verify_password_hash


router = APIRouter(
        prefix="/auth",
        tags=["Authentication"]
        )


u = UserInDB(username="test", hashed_password=create_password_hash("password"))

fake_db: dict[str, str] = {u.username: u.hashed_password}
print(fake_db)


@router.post("/register")
def register(creds: UserCreds, response: Response):

    # Нужно добавить проверку на существование в БД
    password_hash = create_password_hash(creds.password)
    user = UserInDB(username=creds.username, hashed_password= password_hash)
    fake_db[user.username] = password_hash
    return "Вы зарегестрированы"


@router.post("/login")
def login(creds: UserCreds, response: Response):
    if not creds.username in fake_db or not verify_password_hash(creds.password, fake_db[creds.username]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    acces_token = create_jwt_acces_token(creds.username)
    create_cookie_auth(acces_token, response)
    return acces_token


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return "You Authorized"


@router.get("/me")
def me(username = Depends(get_username)):
    return username


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("access_token_cookie")
    #Возможно нужно удалять из security




