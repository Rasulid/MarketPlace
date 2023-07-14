from typing import List

from fastapi import APIRouter, Depends, status, Body, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import ProductModel, Promocode
from api.models.order_model import Order, OrderedProduct
from api.schemas.order_schema import OrderedProductSchema, OrderSchema, OrderSchemaRead
from api.models.user_model import UserModel
from api.auth.login import get_current_user
from api.schemas.promocode_schema import  PromocodeReadSchemaV2

router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")

def find_procent(cash, procent) -> int:
    result_price = cash * (procent / 100)
    return result_price

async def create_order(
        order_schema: OrderSchema,
        product_id: int,
        user_id: int,
        db: Session = Depends(get_db),
        promocode_name: str = Body(default="NONE")
):
    query = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    query_to_promocode = db.query(Promocode).filter(Promocode.name == promocode_name).first()
    if query is None or user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="user or product is invalid"
        )
    if query.count < order_schema.count:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="there are not enough products available"
        )
    if query_to_promocode is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Invalid Promocode"
        )

    order = Order(
        payment_method=order_schema.payment_method,
        total_price=query.price * order_schema.count,
        order_status=order_schema.order_status,
        user_id=user_id,
        count=order_schema.count,
        promocode=query_to_promocode.id

    )
    order_TP = order.total_price
    promocode_price = query_to_promocode.procent
    result_price = 0

    if query_to_promocode.name == 'ALL':
        result_price = find_procent(order_TP, promocode_price)
    elif query_to_promocode.name == promocode_name:
        result_price = find_procent(order_TP, promocode_price)
    elif query_to_promocode.name == 'NONE':
        result_price = find_procent(order_TP, promocode_price)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Promocode not found")

    order.total_price = result_price
    query.count -= order.count

    if query.procent_sale is not None:
        order.total_price = find_procent(order.total_price, query.procent_sale)

    db.add_all([query, order])
    db.commit()

    db.query(OrderedProduct).filter(OrderedProduct.product_id == product_id).delete()

    order_products = []
    for _ in range(order.count):
        ordered_prod = OrderedProduct()
        ordered_prod.product_id = product_id
        ordered_prod.order_id = order.id

        db.add(ordered_prod)
        db.commit()

        order_products.append(OrderedProductSchema(
            product_id=ordered_prod.product_id,
            order_id=ordered_prod.order_id
        ))

    response = OrderSchemaRead(
        id=order.id,
        payment_method=order.payment_method,
        total_price=order.total_price,
        order_status=order.order_status,
        user_id=order.user_id,
        order_products=order_products,
        promocode=[PromocodeReadSchemaV2(id=query_to_promocode.id,
                                         name=query_to_promocode.name,
                                         procent=query_to_promocode.procent)]
    )

    return response


async def order_list_by_user_id(db: Session = Depends(get_db),
                                login: dict = Depends(get_current_user)
                                ):
    id = login.get("user_id")

    query = db.query(Order, OrderedProduct) \
        .join(OrderedProduct, Order.id == OrderedProduct.order_id) \
        .join(Promocode, Order.promocode == Promocode.id)\
        .filter(Order.user_id == id) \
        .all()


    orders_with_products = []
    current_order = None
    current_ordered_products = []
    for order, ordered_product in query:
        print(122,order.promocode_rel)
        if current_order is None or current_order.id != order.id:
            if current_order is not None:
                orders_with_products.append(OrderSchemaRead(
                    id=current_order.id,
                    payment_method=current_order.payment_method,
                    total_price=current_order.total_price,
                    order_status=current_order.order_status,
                    user_id=current_order.user_id,
                    order_products=current_ordered_products,
                    promocode=[PromocodeReadSchemaV2(id=order.promocode_rel.id,
                                         name=order.promocode_rel.name,
                                         procent=order.promocode_rel.procent)]
                ))
            current_order = order
            current_ordered_products = []
        current_ordered_products.append(OrderedProductSchema(
            product_id=ordered_product.product_id,
            order_id=ordered_product.order_id
        ))

    if current_order is not None:
        orders_with_products.append(OrderSchemaRead(
            id=current_order.id,
            payment_method=current_order.payment_method,
            total_price=current_order.total_price,
            order_status=current_order.order_status,
            user_id=current_order.user_id,
            order_products=current_ordered_products,
            promocode=[PromocodeReadSchemaV2(id=order.promocode_rel.id,
                                             name=order.promocode_rel.name,
                                             procent=order.promocode_rel.procent)]
        ))

    return orders_with_products
