import json
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Product_Image_Schema(BaseModel):
    file_name: str
    file_path: str



class Product_Schema(BaseModel):
    title: str
    desc: str
    category: str
    created_at: datetime
    count: int
    procent_sale: int
    promocode: str
    colour: str


class Product_Schema_Read(BaseModel):
    title: str = Field(...)
    desc: str = Field(...)
    category: str = Field(...)
    images: List[Product_Image_Schema] = Field(...)
    owner: int = Field(...)
    created_at: datetime = Field(...)
    count: int = Field(...)
    procent_sale: int = Field(...)
    promocode: str = Field(...)
    colour: str = Field(...)

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
