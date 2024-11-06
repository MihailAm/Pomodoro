from dataclasses import dataclass

from app.repository.category import CatRepository
from app.schema import CatCrateSchema, Category




@dataclass
class CategoryService:
    cat_repository: CatRepository

    async def create_category(self, body: CatCrateSchema):
        cat_id = await self.cat_repository.create_cat(body)
        cat = await self.cat_repository.get_cat(cat_id)
        return Category.model_validate(cat)

    async def all_categories(self):
        cats = await self.cat_repository.get_cats()
        cat_schema = [Category.model_validate(cat) for cat in cats]
        return cat_schema

    async def category_by_id(self, cat_id):
        cat = await self.cat_repository.get_cat(cat_id)
        return Category.model_validate(cat)

    async def update_category_name(self, cat_id, name):
        cat_update = await self.cat_repository.update_cat_name(cat_id=cat_id, name=name)
        return Category.model_validate(cat_update)

    async def delete_category(self, cat_id):
        await self.cat_repository.delete_category(cat_id=cat_id)
