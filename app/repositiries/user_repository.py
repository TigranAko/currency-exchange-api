from sqlalchemy import select

from app.models.user import User

from .base_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    def get_by_name(self, name):
        stmt = select(self.model).where(self.model.username == name)
        result = self.db.execute(stmt).scalar()
        print(result)
        return result

    def update():
        # feature: set user info (password, username)
        pass

    def delete():
        # feature: delete account
        pass
