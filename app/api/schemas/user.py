from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreds(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class UserResponse(BaseModel):
    ok: bool = False
    message: str | None = None
    data: dict | None = None
