from datetime import datetime
from typing import List

from pydantic import BaseModel


class Product_Schema(BaseModel):
    title: str
    desc: str
    category: str
    photos: str
    created_at: datetime
    count: int
    procent_sale: int
    promocode: str
    colour: str


class Product_Schema_Read(BaseModel):
    title: str
    desc: str
    category: str
    photos: List[str]
    owner: int
    created_at: datetime
    count: int
    procent_sale: int
    promocode: str
    colour: str

    class Config:
        orm_mode = True
