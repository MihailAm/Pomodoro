from fastapi import FastAPI, APIRouter, status
from fixtures import categories as cats
from schema.category import Category

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/all",
            response_model=list[Category])
async def get_category():
    return cats


@router.post("/",
             response_model=Category)
async def create_category(cat: Category):
    cats.append(cat)
    return cat


@router.patch("/cat_id}",
              response_model=Category)
async def update_category(cat_id: int, name: str):
    for cat in cats:
        if cat["id"] == cat_id:
            cat["name"] = name
            return cat

