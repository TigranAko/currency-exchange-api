from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreds(UserBase):
    password: str


class UserInDB(UserCreds):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    ok: bool = False
    message: str | None = None
    data: dict | None = None
