import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Product_Image_Schema(BaseModel):
    file_name: str
    file_path: str


class Product_Schema_Read(BaseModel):
    title: str
    desc: str
    category: str
    owner: int
    created_at: datetime
    count: int
    procent_sale: Optional[int]
    promocode: Optional[str]
    colour: str
    images: List[Product_Image_Schema]

    class Config:
        orm_mode = True


class Product_Schema(BaseModel):
    title: str
    desc: str
    category: str
    created_at: datetime
    count: int
    procent_sale: Optional[int]
    promocode: Optional[str]
    colour: str


    class Config:
        orm_mode = True


class AStudentWorkCreateSchema(Product_Schema):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
