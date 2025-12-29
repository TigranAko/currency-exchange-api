from app.api.schemas.user import UserRead
from app.models.user import User
from app.repositiries.user_repository import UserRepository


def test_get_user_by_name(get_session_db):
    repo = UserRepository(get_session_db)
    user = {"username": "username", "password": "password"}
    entity_id = repo.create(user)
    assert isinstance(entity_id, int)
    user_from_db = repo.get_by_name(user["username"])
    assert isinstance(user_from_db, User)
    user_read = UserRead.model_validate(user_from_db)
    assert user_read.password == user["password"]
