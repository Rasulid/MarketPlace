import os
import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File, Body, HTTPException
from fastapi.responses import JSONResponse

from api.schemas.product_schema import ProductImageSchema, \
    AStudentWorkCreateSchema, ProductSchemaReadV2
from sqlalchemy.orm import Session, joinedload
from api.db.session import get_db
from api.models.product_model import ProductModel, ProductImage, CategoryModel, ColourModel, ColourProduct, Promocode
from api.auth.login import get_current_staff
from api.auth.admin_auth import get_user_exceptions
from api.schemas.category_schema import CategorySchema
from api.schemas.colour_schema import ProductColourSchema
from api.schemas.promocode_schema import PromocodeReadSchema

router = APIRouter(
    tags=["Product"],
    prefix="/api/products"
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
        login: dict = Depends(get_current_staff),
):
    if login is None:
        return get_user_exceptions()

    owner_id = login.get("user_id")
    res = []
    upload_image = await upload_img(file)

    result = []

    product_model = ProductModel()
    product_model.title = product.title
    product_model.owner = owner_id
    product_model.description = product.description
    product_model.category_id = product.category_id
    product_model.created_at = product.created_at
    product_model.count = product.count
    product_model.procent_sale = product.procent_sale
    product_model.promocode_id = product.promocode_id
    product_model.price = product.price

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == product_model.category_id).first()

    query_to_promocode = db.query(Promocode).filter(Promocode.id == product_model.promocode_id).first()

    if query_to_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category is empty"
        )

    if query_to_promocode is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="promocode is empty"
        )

    for x in product.colours:
        query_to_colour = db.query(ColourModel).filter(ColourModel.id == x).first()
        if query_to_colour is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="colour is empty"
            )

    db.add(product_model)
    db.commit()
    res.append(product_model)

    colour_data = []
    for x in product.colours:
        colour_products = ColourProduct()
        colour_products.product_id = product_model.id
        colour_products.colour_id = x
        colour_data.append(colour_products)

    db.add_all(colour_data)
    db.commit()

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
        image_data = ProductImageSchema(
            file_name=image.file_name,
            file_path=image.file_path
        )
        images_data.append(image_data)

    product_data = ProductSchemaReadV2(
        id=product_model.id,
        title=product.title,
        description=product.description,
        category=[CategorySchema(id=product.category_id,
                                 title=query_to_category.title)],
        images=images_data,
        owner=product_model.owner,
        created_at=product_model.created_at,
        count=product_model.count,
        procent_sale=product_model.procent_sale,
        promocode=[PromocodeReadSchema(id=query_to_promocode.id, name=query_to_promocode.name,
                                       procent=query_to_promocode.procent, category=[query_to_promocode.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id,
                                    colour_id=colour.colour_id) for colour in colour_data],
        price=product_model.price
    )

    return product_data


@router.get("/list-product", response_model=List[ProductSchemaReadV2])
async def product_list(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)
                       ):
    if login is None:
        return get_user_exceptions()

    query = (
        db.query(ProductModel)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .join(CategoryModel, ProductModel.category_id == CategoryModel.id)
        .join(ColourProduct, ProductModel.id == ColourProduct.product_id)
        .join(Promocode, ProductModel.promocode_id == Promocode.id)
        .options(joinedload(ProductModel.images))
        .all()
    )
    products = []
    for product in query:
        images = [
            ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
            for image in product.images]

        category = [CategorySchema(id=product.category_rel.id, title=product.category_rel.title)]

        colour = [
            ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
            for colour in product.colour_products_rel
        ]

        promocode = [PromocodeReadSchema(id=product.promocode_rel.id,
                                         name=product.promocode_rel.name,
                                         procent=product.promocode_rel.procent,
                                         category=[product.promocode_rel.category_rel])]

        product_data = ProductSchemaReadV2(
            id=product.id,
            title=product.title,
            description=product.description,
            category=category,
            owner=product.owner,
            created_at=product.created_at,
            count=product.count,
            procent_sale=product.procent_sale,
            promocode=promocode,
            colour=colour,
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

    product_model = db.query(ProductModel).filter(ProductModel.id == id).first()

    if product_model is not None:
        product_model.title = product.title
        product_model.owner = owner_id
        product_model.description = product.description
        product_model.category_id = product.category_id
        product_model.created_at = product.created_at
        product_model.count = product.count
        product_model.procent_sale = product.procent_sale
        product_model.promocode_id = product.promocode_id
        product_model.price = product.price
        res.append(product_model)

        file_path = "static/image"
        image_models = db.query(ProductImage).filter(ProductImage.product_id == id).all()
        for image in image_models:
            if image.file_name:
                file_name = os.path.join(file_path, image.file_name)
                if os.path.exists(file_name):
                    os.remove(file_name)
        db.query(ProductImage).filter(ProductImage.product_id == id).delete()

        new_image_models = []
        for x in upload_image:
            new_image = ProductImage(
                file_path=x.file_path,
                file_name=x.file_name,
                product_id=product_model.id
            )
            new_image_models.append(new_image)

        db.add_all(new_image_models)
        db.commit()

        product_model.images = new_image_models

        db.add_all(result)
        db.commit()
        db.add(product_model)
        db.commit()

        images_data = []
        for image in new_image_models:
            image_data = ProductImageSchema(
                file_name=image.file_name,
                file_path=image.file_path
            )
            images_data.append(image_data)

        query_to_category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
        colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == id).delete()
        colour_data = []
        for x in product.colours:
            colour_products = ColourProduct()
            colour_products.product_id = product_model.id
            colour_products.colour_id = x
            colour_data.append(colour_products)

        db.add_all(colour_data)
        db.commit()

        promocode = db.query(Promocode).filter(Promocode.id == product.promocode_id).first()

        product_data = ProductSchemaReadV2(
            id=product_model.id,
            title=product.title,
            description=product.description,
            category=[CategorySchema(id=product.category_id, title=query_to_category.title)],
            images=images_data,
            owner=product_model.owner,
            created_at=product_model.created_at,
            count=product_model.count,
            procent_sale=product_model.procent_sale,
            promocode=[PromocodeReadSchema(id=promocode.id, name=promocode.name,
                                           procent=promocode.procent, category=[promocode.category_rel])],
            colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                    for colour in colour_data],
            price=product_model.price
        )

        return product_data

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Product not found"
    )


@router.delete("/delete/{id}")
async def delete_product(id: int,
                         db: Session = Depends(get_db),
                         login: dict = Depends(get_current_staff)
                         ):
    if login is None:
        return get_user_exceptions()

    chack = db.query(ProductModel) \
        .filter(ProductModel.id == id) \
        .first()

    if chack is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Product not found"
        )

    file_path = f"static/image"
    images = db.query(ProductImage).filter(ProductImage.product_id == id).all()
    for image in images:
        if image.file_name:
            file_name = os.path.join(file_path, image.file_name)
            if os.path.exists(file_name):
                os.remove(file_name)

    db.query(ProductImage).filter(ProductImage.product_id == id).delete()

    query = db.query(ProductModel) \
        .filter(ProductModel.id == id) \
        .delete()

    db.commit()
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content="Product deleted successfully"
    )


@router.get("/get/{id}/", response_model=List[ProductSchemaReadV2])
async def product_list(id: int,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)
                       ):
    if login is None:
        return get_user_exceptions()

    query = (
        db.query(ProductModel)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .join(CategoryModel, ProductModel.category_id == CategoryModel.id)
        .join(ColourProduct, ProductModel.id == ColourProduct.product_id)
        .join(Promocode, ProductModel.promocode_id == Promocode.id)
        .options(joinedload(ProductModel.images))
        .filter(ProductModel.id == id)
        .first()
    )

    if query is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Product {id} not found"
        )

    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in query.images
    ]

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == query.category_id).first()

    colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == query.id).all()

    product_data = ProductSchemaReadV2(
        id=query.id,
        title=query.title,
        description=query.description,
        category=[CategorySchema(id=query.category_id, title=query_to_category.title)],
        images=images,
        owner=query.owner,
        created_at=query.created_at,
        count=query.count,
        procent_sale=query.procent_sale,
        promocode=[PromocodeReadSchema(id=query.promocode_rel.id,
                                         name=query.promocode_rel.name,
                                         procent=query.promocode_rel.procent,
                                         category=[query.promocode_rel.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                for colour in colour_data],
        price=query.price
    )

    return [product_data]
