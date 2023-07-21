from datetime import date

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    # id: int
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


class UserSchema(BaseModel):
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


class UserSchemaRead(BaseModel):
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
