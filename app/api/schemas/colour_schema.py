from pydantic import BaseModel


class ColourSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
