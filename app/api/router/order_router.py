from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import ProductModel
from api.models.order_model import Order, OrderedProduct
from api.schemas.order_schema import OrderedProductSchema, OrderSchema, OrderSchemaRead
from api.models.user_model import UserModel

router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")


@router.post('/create', response_model=List[OrderSchemaRead])
async def create_order(user_id: int,
                       product_id: int,
                       order_schema: OrderSchema,
                       ordered_product_schema: List[OrderedProductSchema],
                       db: Session = Depends(get_db)):
    query_to_prod = db.query(ProductModel) \
        .filter(ProductModel.id == product_id) \
        .first()

    query_to_user = db.query(UserModel) \
        .filter(UserModel.id == user_id) \
        .first()

    if query_to_prod is None or query_to_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Not Found")

    order = Order()
    order.payment_method = order_schema.payment_method
    order.total_price = query_to_prod.price
    order.order_status = order_schema.order_status
    order.user_id = user_id
    order.count = order_schema.count
    # order.ordered_products = ordered_prod

    order_count = order.count

    # db.add(order)
    # db.commit()
    for product in range(order_count):
        count = 1
        ordered_prod = OrderedProduct()
        ordered_prod.product_id = query_to_prod.id
        ordered_prod.order_id = order.id

        count += 1
        # db.add(ordered_prod)
        # db.commit()

    return order


@router.post('/create_test', response_model=OrderSchemaRead)
async def create_order(order_schema: OrderSchema,
                       product_id: int,
                       user_id: int,
                       ordered_product_schema: OrderedProductSchema,
                       db: Session = Depends(get_db)):
    query_to_prod = db.query(ProductModel) \
        .filter(ProductModel.id == product_id) \
        .first()

    query_to_user = db.query(UserModel) \
        .filter(UserModel.id == user_id) \
        .first()

    if query_to_prod is None or query_to_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Not Found")

    order = Order()
    order.payment_method = order_schema.payment_method
    order.total_price = query_to_prod.price
    order.order_status = order_schema.order_status
    order.user_id = user_id
    order.count = order_schema.count

    db.add(order)
    db.commit()

    order_products = []
    print(order.count)
    for ordered_product in range(order.count):
        ordered_prod = OrderedProduct()
        ordered_prod.product_id = product_id
        ordered_prod.order_id = order.id



        db.add(ordered_prod)
        db.commit()

        order_products.append(OrderedProductSchema(
            product_id=ordered_prod.product_id,
            order_id=ordered_prod.order_id
        ))

    t_p = order.total_price * order.count
    response = OrderSchemaRead(
        payment_method=order.payment_method,
        total_price=t_p,
        order_status=order.order_status,
        user_id=order.user_id,
        order_products=order_products
    )

    return response
