from pydantic import BaseModel


class PromocodeSchema(BaseModel):
    name: str
    procent: int


class PromocodeReadSchema(BaseModel):
    id: int
    name: str
    procent: int

    class Config:
        orm_mode = True