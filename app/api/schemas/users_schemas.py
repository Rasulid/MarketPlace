from datetime import date


from pydantic import BaseModel


class User_Schema(BaseModel):
    id: int
    name: str
    l_name: str
    born: date
    phone_number: str
    country: str = "UZB"
    region: str
    gmail: str
    password: str

    class Config:
        orm_mode = True

class User_Schema_Read(BaseModel):
    id: int
    name: str
    l_name: str
    born: date
    phone_number: str
    country: str = "UZB"
    region: str
    gmail: str
    password: str

    class Config:
        orm_mode = True
