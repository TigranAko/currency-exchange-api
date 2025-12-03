from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import BaseModel
from app.models.user import User

print(User)

# TODO: use env file
# TODO: other DB fpr tests

url = "sqlite:///test.db"

engine = create_engine(url=url, echo=True)

Session = sessionmaker(engine, autoflush=False)


def create_tables():
    BaseModel.metadata.create_all(engine)


def delete_tables():
    BaseModel.metadata.drop_all(engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
