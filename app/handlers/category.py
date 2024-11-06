from typing import Annotated

from fastapi import FastAPI, APIRouter, status, Depends

from app.dependecy import get_cat_service
from app.schema import CatCrateSchema
from app.schema.category import Category
from app.service import CategoryService

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/all",
            response_model=list[Category])
async def get_category(cat_service: Annotated[CategoryService, Depends(get_cat_service)]):
    cats = await cat_service.all_categories()
    return cats


@router.post("/",
             response_model=Category)
async def create_category(cat_service: Annotated[CategoryService, Depends(get_cat_service)],
                          cat: CatCrateSchema):
    new_cat = await cat_service.create_category(cat)
    return new_cat


@router.patch("/{cat_id}",
              response_model=Category)
async def update_category(cat_id: int, name: str,
                          cat_service: Annotated[CategoryService, Depends(get_cat_service)]):
    update_cat_name = await cat_service.update_category_name(cat_id=cat_id, name=name)
    return update_cat_name


@router.delete("/{cat_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(cat_id: int,
                      cat_service: Annotated[CategoryService, Depends(get_cat_service)]):
    await cat_service.delete_category(cat_id=cat_id)
