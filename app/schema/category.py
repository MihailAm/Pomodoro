from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id: int
    type: str | None = None
    name: str

    model_config = ConfigDict(from_attributes=True)


class CatCrateSchema(BaseModel):
    type: str | None = None
    name: str