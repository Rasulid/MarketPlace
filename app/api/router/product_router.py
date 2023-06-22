import os
import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from api.schemas.product_schema import Product_Image_Schema, \
    AStudentWorkCreateSchema, Product_Schema_Read_V2
from sqlalchemy.orm import Session, joinedload
from api.db.session import get_db
from api.models.product_model import Product_Model, Product_Image
from api.auth.login import get_current_staff
from api.auth.admin_auth import get_user_exceptions

router = APIRouter(
    tags=["Product"],
    prefix="/api/product"
)


async def upload_img(file: List[UploadFile] = File(...)):
    image_list = []
    for img in file:
        img.filename = f"{uuid.uuid4()}.jpg"
        with open(f"static/image/{img.filename}", "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
            append_for_db = Product_Image_Schema(file_name=img.filename, file_path=f"static/image")
        image_list.append(append_for_db)
    return image_list


@router.post("/create", response_model=Product_Schema_Read_V2)
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

    db.add(product_model)
    db.commit()
    res.append(product_model)

    for x in upload_image:
        image_model = Product_Image()
        image_model.file_path = x.file_path
        image_model.file_name = x.file_name
        image_model.product_id = product_model.id

        result.append(image_model)

    db.add_all(result)
    db.commit()

    images_data = []
    for image in result:
        image_data = Product_Image_Schema(file_name=image.file_name,
                                          file_path=image.file_path)
        images_data.append(image_data)

    product_data = Product_Schema_Read_V2(
        title=product.title,
        desc=product.desc,
        category=product.category,
        images=images_data,
        owner=product_model.owner,
        created_at=product_model.created_at,
        count=product_model.count,
        procent_sale=product_model.procent_sale,
        promocode=product_model.promocode,
        colour=product_model.colour,
    )

    return product_data


@router.get("/list-product", response_model=List[Product_Schema_Read_V2])
async def product_list(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    query = (
        db.query(Product_Model)
        .join(Product_Image, Product_Model.id == Product_Image.product_id)
        .options(joinedload(Product_Model.images))
        .all()
    )
    products = []
    for product in query:
        images = [
            Product_Image_Schema(file_name=image.file_name, file_path=image.file_path)
            for image in product.images]

        product_data = Product_Schema_Read_V2(
            title=product.title,
            desc=product.desc,
            category=product.category,
            owner=product.owner,
            created_at=product.created_at,
            count=product.count,
            procent_sale=product.procent_sale,
            promocode=product.promocode,
            colour=product.colour,
            images=images
        )
        products.append(product_data)

    return products



@router.put("/update")
async def update_product(
        id: int,
        product: AStudentWorkCreateSchema,
        db: Session = Depends(get_db),
        file: List[UploadFile] = File(),
        # login: dict = Depends(get_current_staff)
):
    # if login is None:
    #     return get_user_exceptions()

    # owner_id = login.get("user_id")
    res = []
    upload_image = await upload_img(file)

    result = []

    query = db.query(Product_Model).filter(Product_Model.id == id).first()

    if query is not None:

        product_model = Product_Model()
        product_model.title = product.title
        product_model.desc = product.desc
        product_model.category = product.category
        product_model.owner = 1
        product_model.created_at = product.created_at
        product_model.count = product.count
        product_model.procent_sale = product.procent_sale
        product_model.promocode = product.promocode
        product_model.colour = product.colour

        # db.add(product_model)
        # db.commit()
        res.append(product_model)

        file_path = f"static/image"
        images = db.query(Product_Image).filter(Product_Image.product_id == id).all()
        for image in images:
            if image.file_name:
                print(image.file_name)
                file_name = os.path.join(file_path, image.file_name)
                if os.path.exists(file_name):
                    os.remove(file_name)
                else:
                    return "File not found"

        for x in upload_image:
            image_model = Product_Image()
            image_model.file_path = x.file_path
            image_model.file_name = x.file_name
            image_model.product_id = product_model.id

            result.append(image_model)

        # db.add_all(result)
        # db.commit()

        images_data = []
        for image in result:
            image_data = Product_Image_Schema(file_name=image.file_name,
                                              file_path=image.file_path)
            images_data.append(image_data)

        product_data = Product_Schema_Read_V2(
            title=product.title,
            desc=product.desc,
            category=product.category,
            images=images_data,
            owner=product_model.owner,
            created_at=product_model.created_at,
            count=product_model.count,
            procent_sale=product_model.procent_sale,
            promocode=product_model.promocode,
            colour=product_model.colour,
        )
        return product_data

    return query


@router.delete("/delete")
async def delete_product(id: int,
                         db: Session = Depends(get_db),
                         login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    chack = db.query(Product_Model)\
        .filter(Product_Model.id == id)\
        .first()

    if chack is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND)

    # Удаление фотографий
    file_path = f"static/image"
    images = db.query(Product_Image).filter(Product_Image.product_id == id).all()
    for image in images:
        if image.file_name:
            file_name = os.path.join(file_path, image.file_name)
            if os.path.exists(file_name):
                os.remove(file_name)

    # Удаление записей о фотографиях в базе данных
    db.query(Product_Image).filter(Product_Image.product_id == id).delete()

    # Удаление товара
    query = db.query(Product_Model)\
        .filter(Product_Model.id == id)\
        .delete()

    db.commit()
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content="Product deleted successfully"
    )
