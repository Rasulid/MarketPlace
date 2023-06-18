import os
import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from api.schemas.product_schema import Product_Schema, Product_Schema_Read
from sqlalchemy.orm import Session
from api.db.session import get_db
from api.models.product_model import Product_Model
from api.auth.login import get_current_staff, get_current_admin
from api.auth.admin_auth import get_user_exceptions

router = APIRouter(
    tags=["Product"],
    prefix="/api/product"
)


@router.post("/create", response_model=List[Product_Schema_Read])
async def create_product(
        product: Product_Schema,
        db: Session = Depends(get_db),
        files: List[UploadFile] = File(...)
):
    res = []
    result = []

    product_model = Product_Model()
    product_model.title = product.title
    product_model.desc = product.desc
    product_model.category = product.category
    product_model.owner = 18
    product_model.created_at = product.created_at
    product_model.count = product.count
    product_model.procent_sale = product.procent_sale
    product_model.promocode = product.promocode
    product_model.colour = product.colour

    db.add(product_model)
    db.commit()

    res.append(product_model)

    for image in files:
        with open(f'static/image/{image.filename}', "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            result.append(f'static/image/{image.filename}')

    product_model.photos = result

    db.commit()

    return res


@router.get("/list-product", response_model=List[Product_Schema_Read])
async def product_list(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    query = db.query(Product_Model).all()

    return query


async def Upload_File(file: List[UploadFile] = File(...)):
    result = []
    for image in file:
        with open(f'static/image/{image.filename}', "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            result.append(image.filename)

    return {"filename": result}
