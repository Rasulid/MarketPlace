from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class Admin_Schema(BaseModel):
    name: str
    born: date
    # created_at: Optional[datetime]
    phone_number: str
    gmail: str
    password: str
    country: str = "UZB"
    region: str
    is_active: bool = True
    is_staff: bool = True
    is_superuser: bool
    is_verified: bool 



class Admin_Read_Schema(BaseModel):
    id: int
    name: str
    born: date
    created_at: datetime
    phone_number: str
    gmail: str
    country: str = "UZB"
    region: str
    is_active: bool = True
    is_staff: bool = True
    is_superuser: bool = False
    is_verified: bool = False


    class Config:
        orm_mode = True