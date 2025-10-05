from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreds(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
