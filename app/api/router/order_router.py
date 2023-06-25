from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.order_model import Order, OrderedProduct
from api.schemas.order_schema import OrderedProductSchema, OrderSchema

router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")

@router.post('/create')
async def create_order(order: OrderSchema,
            db: Session = Depends(get_db)):

    order_model = Order()
    order_model.payment_method = order.payment_method
    order_model.total_price = order.total_price
    order_model.order_status = order.order_status
    order_model.user_id = 1


