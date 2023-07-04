from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
