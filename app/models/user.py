from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
