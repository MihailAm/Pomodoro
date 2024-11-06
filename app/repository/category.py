from dataclasses import dataclass

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Categories
from app.schema import CatCrateSchema


@dataclass
class CatRepository:
    db_session: AsyncSession

    async def get_cats(self) -> list[Categories]:
        async with self.db_session as session:
            result = await session.execute(select(Categories))
            cat: list[Categories] = list(result.scalars().all())
        return cat

    async def get_cat(self, cat_id: int) -> Categories | None:
        async with self.db_session as session:
            cat: Categories = (
                await session.execute(select(Categories).where(Categories.id == cat_id))).scalar_one_or_none()
        return cat

    async def create_cat(self, cat: CatCrateSchema) -> int:
        cat_model = Categories(name=cat.name,
                               type=cat.type
                               )
        async with self.db_session as session:
            session.add(cat_model)
            await session.commit()
            return cat_model.id

    async def update_cat_name(self, cat_id, name):
        query = update(Categories).where(Categories.id == cat_id).values(name=name).returning(Categories.id)

        async with self.db_session as session:
            category_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_cat(category_id)

    async def delete_category(self, cat_id: int) -> None:
        query = delete(Categories).where(Categories.id == cat_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
