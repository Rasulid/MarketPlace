from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import ProductModel
from api.models.order_model import Order, OrderedProduct
from api.schemas.order_schema import OrderedProductSchema, OrderSchema
from api.models.user_model import UserModel

router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")


@router.post('/create')
async def create_order(user_id: int,
                       product_id: int,
                       order_schema: OrderSchema,
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

    print(query_to_prod.price)

    ordered_prod = [OrderedProductSchema(
        product_id=query_to_prod.id,
        order_id=1,
        count=1
    )]

    # ordered_products = [ordered_prod]  # Создаем список с одним элементом

    order = Order()
    order.payment_method = order_schema.payment_method
    order.total_price = query_to_prod.price
    order.order_status = order_schema.order_status
    order.user_id = user_id
    order.ordered_products = ordered_prod
    print(order.id)

    return order