from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Admin_Schema(BaseModel):
    name: str
    age: int
    created_at: datetime
    phone_number: str
    gmail: Optional[str] = None
    password: str
    country: str = "UZB"
    region: str
    is_active: bool = True
    is_staff: bool = True
    is_superuser: bool = False
    is_verified: bool = False
