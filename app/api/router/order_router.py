from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import ProductModel
from api.models.order_model import Order, OrderedProduct
from api.schemas.order_schema import OrderedProductSchema, OrderSchema, OrderSchemaRead
from api.models.user_model import UserModel
from api.auth.login import get_current_user

router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")


@router.post('/create', response_model=OrderSchemaRead)
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


@router.get('/orders/{id}', response_model=List[OrderSchemaRead])
async def order_list_by_user_id(id: int, db: Session = Depends(get_db),
                     login: dict = Depends(get_current_user)):
    query = (
        db.query(Order, OrderedProduct)
        .join(OrderedProduct, Order.id == OrderedProduct.order_id)
        .filter(Order.user_id == id)
        .all()
    )

    orders_with_products = []
    current_order = None
    current_ordered_products = []
    for order, ordered_product in query:
        if current_order is None or current_order.id != order.id:
            if current_order is not None:
                orders_with_products.append(OrderSchemaRead(
                    payment_method=current_order.payment_method,
                    total_price=current_order.total_price,
                    order_status=current_order.order_status,
                    user_id=current_order.user_id,
                    order_products=current_ordered_products
                ))
            current_order = order
            current_ordered_products = []
        current_ordered_products.append(OrderedProductSchema(
            product_id=ordered_product.product_id,
            order_id=ordered_product.order_id
        ))

    if current_order is not None:
        orders_with_products.append(OrderSchemaRead(
            payment_method=current_order.payment_method,
            total_price=current_order.total_price,
            order_status=current_order.order_status,
            user_id=current_order.user_id,
            order_products=current_ordered_products
        ))

    return orders_with_products