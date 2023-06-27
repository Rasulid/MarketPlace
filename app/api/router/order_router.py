from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import ProductModel
from api.models.order_model import Order, OrderedProduct
from api.schemas.order_schema import OrderedProductSchema, OrderSchema

router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")

@router.post('/create')
async def create_order(user_id:int,
                       product_id:int,
                       db: Session = Depends(get_db)):

    query_to_prod = db.query(ProductModel)




