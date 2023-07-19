from typing import List

from pydantic import BaseModel

from api.schemas.category_schema import CategorySchema


class PromocodeSchema(BaseModel):
    name: str
    procent: int
    category: int


class PromocodeReadSchema(BaseModel):
    id: int
    name: str
    procent: int
    category: List[CategorySchema]

    class Config:
        orm_mode = True


class PromocodeReadSchemaV2(BaseModel):
    id: int
    name: str
    procent: int
