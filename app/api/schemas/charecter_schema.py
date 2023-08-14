from typing import List

from pydantic import BaseModel

from api.schemas.product_schema import ProductSchemaReadV2


class MobileCharSchema(BaseModel):
    colour: str
    processor: str
    memory: str
    charger: str
    front_cam: str
    main_cam: str
    hrz: str
    display: str
    type_display: str


class MobileCharSchemaRead(BaseModel):
    id: int
    product_id: List[ProductSchemaReadV2]
    colour: str
    processor: str
    memory: str
    charger: str
    front_cam: str
    main_cam: str
    hrz: str
    display: str
    type_display: str


class MobileCharSchemaReadV2(BaseModel):
    id: int
    product_id: int
    colour: str
    processor: str
    memory: str
    charger: str
    front_cam: str
    main_cam: str
    hrz: str
    display: str
    type_display: str

    class Config:
        orm_mode = True


class CompCharSchema(BaseModel):
    colour: str
    processor: str
    memory: str
    display: str
    memory_type: str
    RAM: str


class CompCharSchemaRead(BaseModel):
    id: int
    product_id: List[ProductSchemaReadV2]
    colour: str
    processor: str
    memory: str
    display: str
    memory_type: str
    RAM: str


class CompCharSchemaReadV2(BaseModel):
    id: int
    product_id: int
    colour: str
    processor: str
    memory: str
    display: str
    memory_type: str
    RAM: str