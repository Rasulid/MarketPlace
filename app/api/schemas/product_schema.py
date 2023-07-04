import json
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from typing import List, Optional
# from pydantic import BaseModel


class ProductImageSchema(BaseModel):
    file_name: str
    file_path: str


class ProductSchemaRead(BaseModel):
    title: str
    desc: str
    category: str
    owner: int
    created_at: datetime
    count: int
    procent_sale: Optional[int]
    promocode: Optional[str]
    colour: str
    price: float
    images: List[ProductImageSchema]

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    title: str
    description: str
    category: str
    created_at: datetime
    count: int
    procent_sale: int
    promocode: str
    procent_sale: Optional[int]
    promocode: Optional[str]
    colour: str
    price: float


class ProductSchemaReadV2(BaseModel):

    title: str
    description: str
    category: str
    images: List[ProductImageSchema]
    owner: int
    created_at: datetime
    count: int
    procent_sale: int
    promocode: str
    colour: str  
    price: float

    class Config:
        orm_mode = True


class AStudentWorkCreateSchema(ProductSchema):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value