import os
import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from api.schemas.product_schema import ProductImageSchema, \
    AStudentWorkCreateSchema, ProductSchemaReadV2
from sqlalchemy.orm import Session, joinedload
from api.db.session import get_db
from api.models.product_model import ProductModel, ProductImage
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
            append_for_db = ProductImageSchema(file_name=img.filename, file_path=f"static/image")
        image_list.append(append_for_db)
    return image_list


@router.post("/create", response_model=ProductSchemaReadV2)
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

    product_model = ProductModel()
    product_model.title = product.title
    product_model.description = product.description
    product_model.category = product.category
    product_model.owner = owner_id
    product_model.created_at = product.created_at
    product_model.count = product.count
    product_model.procent_sale = product.procent_sale
    product_model.promocode = product.promocode
    product_model.colour = product.colour
    product_model.price = product.price

    db.add(product_model)
    db.commit()
    res.append(product_model)

    for x in upload_image:
        image_model = ProductImage()
        image_model.file_path = x.file_path
        image_model.file_name = x.file_name
        image_model.product_id = product_model.id

        result.append(image_model)

    db.add_all(result)
    db.commit()

    images_data = []
    for image in result:
        image_data = ProductImageSchema(file_name=image.file_name,
                                          file_path=image.file_path)
        images_data.append(image_data)

    product_data = ProductSchemaReadV2(
        title=product.title,
        description=product.description,
        category=product.category,
        images=images_data,
        owner=product_model.owner,
        created_at=product_model.created_at,
        count=product_model.count,
        procent_sale=product_model.procent_sale,
        promocode=product_model.promocode,
        colour=product_model.colour,
        price=product_model.price
    )

    return product_data


@router.get("/list-product", response_model=List[ProductSchemaReadV2])
async def product_list(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    query = (
        db.query(ProductModel)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .options(joinedload(ProductModel.images))
        .all()
    )
    products = []
    for product in query:
        images = [
            ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
            for image in product.images]

        product_data = ProductSchemaReadV2(
            title=product.title,
            description=product.description,
            category=product.category,
            owner=product.owner,
            created_at=product.created_at,
            count=product.count,
            procent_sale=product.procent_sale,
            promocode=product.promocode,
            colour=product.colour,
            images=images,
            price=product.price
        )
        products.append(product_data)

    return products



@router.put("/update/{id}")
async def update_product(
        id: int,
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

    query = db.query(ProductModel).filter(ProductModel.id == id).first()

    if query is not None:

        product_model = ProductModel()
        product_model.title = product.title
        product_model.description = product.description
        product_model.category = product.category
        product_model.owner = 1
        product_model.created_at = product.created_at
        product_model.count = product.count
        product_model.procent_sale = product.procent_sale
        product_model.promocode = product.promocode
        product_model.colour = product.colour
        product_model.price = product.price

        db.add(product_model)
        db.commit()
        res.append(product_model)

        file_path = f"static/image"
        images = db.query(ProductImage).filter(ProductImage.product_id == id).all()
        for image in images:
            if image.file_name:
                print(image.file_name)
                file_name = os.path.join(file_path, image.file_name)
                if os.path.exists(file_name):
                    os.remove(file_name)
                else:
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content="Photo not Found"
                    )

        for x in upload_image:
            image_model = ProductImage()
            image_model.file_path = x.file_path
            image_model.file_name = x.file_name
            image_model.product_id = product_model.id

            result.append(image_model)

        db.add_all(result)
        db.commit()
        images_data = []
        for image in result:
            image_data = ProductImageSchema(file_name=image.file_name,
                                              file_path=image.file_path)
            images_data.append(image_data)

        product_data = ProductSchemaReadV2(
            title=product.title,
            ription=product.ription,
            category=product.category,
            images=images_data,
            owner=product_model.owner,
            created_at=product_model.created_at,
            count=product_model.count,
            procent_sale=product_model.procent_sale,
            promocode=product_model.promocode,
            colour=product_model.colour,
            price=product_model.price
        )
        return product_data

    return query


@router.delete("/delete/{id}")
async def delete_product(id: int,
                         db: Session = Depends(get_db),
                         login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    chack = db.query(ProductModel)\
        .filter(ProductModel.id == id)\
        .first()

    if chack is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Product not found"
        )

    # Удаление фотографий
    file_path = f"static/image"
    images = db.query(ProductImage).filter(ProductImage.product_id == id).all()
    for image in images:
        if image.file_name:
            file_name = os.path.join(file_path, image.file_name)
            if os.path.exists(file_name):
                os.remove(file_name)

    # Удаление записей о фотографиях в базе данных
    db.query(ProductImage).filter(ProductImage.product_id == id).delete()

    # Удаление товара
    query = db.query(ProductModel)\
        .filter(ProductModel.id == id)\
        .delete()

    db.commit()
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content="Product deleted successfully"
    )


@router.get("/{id}/", response_model=List[ProductSchemaReadV2])
async def product_list(id: int,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    query = (
        db.query(ProductModel)
        .filter(ProductModel.id == id)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .options(joinedload(ProductModel.images))
        .first()
    )

    if query is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"product {id} not Found"
        )

    products = []

    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in query.images]

    product_data = ProductSchemaReadV2(
        title=query.title,
        description=query.description,
        category=query.category,
        owner=query.owner,
        created_at=query.created_at,
        count=query.count,
        procent_sale=query.procent_sale,
        promocode=query.promocode,
        colour=query.colour,
        images=images,
        price=query.price,
    )
    products.append(product_data)

    return products
