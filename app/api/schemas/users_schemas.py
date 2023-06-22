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
    created_at: datetime
    is_active: bool = True
    is_verified: bool = False
    update_at: datetime

    class Config:
        orm_mode = True
