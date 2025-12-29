from app.dependencies.database import BaseModel
from app.models.user import User
from app.repositiries.base_repository import SQLAlchemyRepository


class ExampleRepository(SQLAlchemyRepository):
    model: BaseModel = User  # any entity


def test_create_read(get_session_db):
    entity = {"username": "example_username", "password": "example_password"}
    repo = ExampleRepository(get_session_db)
    start_entities = repo.get_all()

    entity_id = repo.create(entity)
    assert isinstance(entity_id, int)
    entity_from_db = repo.get_by_id(entity_id)
    assert isinstance(entity_from_db, repo.model)
    finish_entities = repo.get_all()
    assert start_entities != finish_entities
    assert isinstance(start_entities, list)
    assert isinstance(finish_entities, list)
    assert len(start_entities) + 1 == len(finish_entities)


# TODO: feature: test for update and delete
