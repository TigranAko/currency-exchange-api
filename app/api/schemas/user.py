from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    username: str | None = None
    # TODO: Пока что не используется


# TODO: Добавить изменение пароля
