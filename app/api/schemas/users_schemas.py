from fastapi_users import schemas


class CreateUser(schemas.BaseUserCreate):
    name: str
    age: int
    phone_number: str
    country: str
    region: str
    is_staff: bool

    class Config:
        orm_mode = True


class ReadUser(schemas.BaseUserCreate):
    name: str
    age: int
    phone_number: str
    country: str
    region: str
    is_staff: bool

    class Config:
        orm_mode = True
