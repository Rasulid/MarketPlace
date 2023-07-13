from datetime import datetime

from pydantic import BaseModel


class User_Schema(BaseModel):
    name: str
    l_name: str
    age: int
    phone_number: str
    country: str = "UZB"
    region: str
    gmail: str
    password: str

    class Config:
        orm_mode = True
