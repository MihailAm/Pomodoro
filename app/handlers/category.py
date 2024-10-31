from fastapi import FastAPI, APIRouter, status
from app.schema.category import Category

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/all",
            response_model=list[Category])
async def get_category():
    pass


@router.post("/",
             response_model=Category)
async def create_category(cat: Category):
    pass


@router.patch("/cat_id}",
              response_model=Category)
async def update_category(cat_id: int, name: str):
    pass

