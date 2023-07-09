from enum import Enum
from pydantic import BaseModel
from typing import List

from api.schemas.promocode_schema import PromocodeReadSchema, PromocodeReadSchemaV2


class PaymentMethod(str, Enum):
    cash = 'cash'
    card = 'card'


class OrderStatus(str, Enum):
    in_the_shop = 'in the shop'
    courier_took = 'courier took'


class OrderedProductSchema(BaseModel):
    product_id: int
    order_id: int


class OrderSchemaRead(BaseModel):
    id: int
    payment_method: PaymentMethod
    total_price: float
    order_status: OrderStatus
    user_id: int
    order_products: List[OrderedProductSchema]
    promocode: List[PromocodeReadSchemaV2]

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    payment_method: PaymentMethod
    order_status: OrderStatus
    count: int
    promocode: int
