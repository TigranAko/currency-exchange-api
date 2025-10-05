
from fastapi import APIRouter, HTTPException, status, Response, Depends
#from fastapi.security.http import HTTPBasicCredentials
from app.api.schemas.user import UserCreds, UserInDB
from app.core.security import create_jwt_acces_token, create_cookie_auth#, get_username
from app.core.security import security, get_username

router = APIRouter(
        prefix="/auth",
        tags=["Authentication"]
        )


u = UserInDB(username="test", hashed_password="test")

fake_db: dict[str, str] = {u.username: u.hashed_password}
print(fake_db)


#def verify_user(user: UserInDB):
#    if user.username != "test" and user.hashed_password != "test":
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#    return True


#def get_user_id(creds: UserCreds):
#    for user in fake_db.values():
#        if user.username == creds.username:
#            return user.user_id
#    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

#def get_user_by_id(user_id):
#    return fake_db[user_id]


@router.post("/register")
def register(creds: UserCreds, response: Response):
    user = UserInDB(username=creds.username, hashed_password= creds.password)


    # HASHING
    fake_db[user.username] = user.hashed_password
    return "Вы зарегестрированы"


@router.post("/login")
def login(creds: UserCreds, response: Response):
#    user_id = get_user_id(creds) #
    if creds.username in fake_db:
        acces_token = create_jwt_acces_token(creds.username)
        create_cookie_auth(acces_token, response) # ТУТ ОШИБКА
        return acces_token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():

    return "You Authorized"

@router.get("/me")
def me(username = Depends(get_username)):
    return username


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("access_token_cookie")




