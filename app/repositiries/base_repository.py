from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.dependencies.database import BaseModel


class SQLAlchemyRepository:
    model: BaseModel

    def __init__(self, session: Session):
        self.db: Session = session

    async def get_by_id(self, entity_id: int):
        stmt = select(self.model).where(entity_id == self.model.id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_all(self):
        stmt = select(self.model).offset(0).limit(10)  # TODO: check offset limit, test
        result = await self.db.execute(stmt)
        return result.all()

    async def create(self, entity: dict):
        stmt = insert(self.model).values(**entity).returning(self.model.id)
        entity_id = await self.db.execute(stmt)
        await self.db.commit()
        return entity_id.scalar_one()


# feature: now not used
#     def update(self, entity):
#         stmt = update(self.model).value(entity).returning(entity.id)
#         entity_id = self.db.execute(stmt)
#         return entity_id.scalar_one()
#
#    def delete(self, entity_id):
#        stmt = delete(self.model).where(self.model.id == entity_id)
#        entity_id = self.db.execute(stmt)
#        return entity_id.scalar_one()
