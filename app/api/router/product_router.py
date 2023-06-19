import os
import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File, Body
from api.schemas.product_schema import Product_Schema, Product_Schema_Read, Product_Image_Schema, \
    AStudentWorkCreateSchema
from sqlalchemy.orm import Session
from api.db.session import get_db
from api.models.product_model import Product_Model, Product_Image
from api.auth.login import get_current_staff, get_current_admin
from api.auth.admin_auth import get_user_exceptions

router = APIRouter(
    tags=["Product"],
    prefix="/api/product"
)


@router.post("/create")
async def create_product(
        product: AStudentWorkCreateSchema,
        db: Session = Depends(get_db),
        file: List[UploadFile] = File(),
        login: dict = Depends(get_current_staff)
):

    if login is None:
        return get_user_exceptions()
    
    owner_id = login.get("user_id")
    res = []
    upload_image = await upload_img(file)

    result = []

    product_model = Product_Model()
    product_model.title = product.title
    product_model.desc = product.desc
    product_model.category = product.category
    product_model.owner = owner_id
    product_model.created_at = product.created_at
    product_model.count = product.count
    product_model.procent_sale = product.procent_sale
    product_model.promocode = product.promocode
    product_model.colour = product.colour

    res.append(product_model)
    db.add(product_model)
    db.commit()

    for x in upload_image:
        image_model = Product_Image()
        image_model.file_path = x.file_path
        image_model.file_name = x.file_name
        image_model.product_id = product_model.id
        res.append(image_model)

    res.append(result)
    db.add_all(result)
    db.commit()

    return res


@router.get("/list-product", response_model=List[Product_Schema_Read])
async def product_list(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    query = db.query(Product_Model).all()

    return query


async def upload_img(file: List[UploadFile] = File(...)):
    image_list = []
    for img in file:
        img.filename = f"{uuid.uuid4()}.jpg"
        with open(f"static/image/{img.filename}", "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
            append_for_db = Product_Image_Schema(file_name=img.filename, file_path=f"static/image")
        image_list.append(append_for_db)
    return image_list


@router.post("/img/")
async def post_img(test_id: int = Body(...),
                   db: Session = Depends(get_db),
                   file: List[UploadFile] = File(...)):
    upload_image = await upload_img(file)

    result = []
    for x in upload_image:
        image_model = Product_Image()
        image_model.file_path = x.file_path
        image_model.file_name = x.file_name
        image_model.product_id = test_id
        result.append(image_model)

    db.add_all(result)
    db.commit()

    return "Success"
