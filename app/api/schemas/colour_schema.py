from pydantic import BaseModel


class ColourSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class ProductColourSchema(BaseModel):
    id: int
    product_id: int
    colour_id: int