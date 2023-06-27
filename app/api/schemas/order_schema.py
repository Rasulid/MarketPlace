from pydantic import BaseModel
from enum import Enum


class PaymentMethod(Enum):
    cash = "cash"
    card = "card"


class OrderStatus(Enum):
    in_the_shop = "in the shop"
    courier_took = "courier took"


class OrderedProductSchema(BaseModel):
    product_id: int
    order_id: int
    count: int


class OrderSchema(BaseModel):
    payment_method: PaymentMethod
    total_price: int
    order_status: OrderStatus
    user_id: int
    # order_products: list[OrderedProductSchema]


class OrderSchemaRead(BaseModel):
    payment_method: PaymentMethod
    total_price: int
    order_status: OrderStatus
    user_id: int
    order_products: list[OrderedProductSchema]