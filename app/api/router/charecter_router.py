from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette.responses import JSONResponse

from api.db.session import get_db
from api.models.charecter import MobileChar, CompChar
from api.schemas.charecter_schema import MobileCharSchemaRead, MobileCharSchema, MobileCharSchemaReadV2, \
    CompCharSchemaRead, CompCharSchema, CompCharSchemaReadV2
from api.auth.login import get_current_staff
from api.models.product_model import ProductModel, ProductImage, CategoryModel, ColourProduct, Promocode
from api.schemas.category_schema import CategorySchema
from api.schemas.colour_schema import ProductColourSchema
from api.schemas.product_schema import ProductSchemaReadV2, ProductImageSchema
from api.schemas.promocode_schema import PromocodeReadSchema

router = APIRouter()



async def create_char_mobile(schema: MobileCharSchema,
                             product_id: int
                             , db: Session = Depends(get_db),
                             login: dict = Depends(get_current_staff)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    model = MobileChar()
    model.colour = schema.colour
    model.product_id = product_id
    model.processor = schema.processor
    model.memory = schema.memory
    model.charger = schema.charger
    model.front_cam = schema.front_cam
    model.main_cam = schema.main_cam
    model.hrz = schema.hrz
    model.display = schema.display
    model.type_display = schema.type_display

    db.add(model)
    db.commit()

    query = (
        db.query(ProductModel)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .join(CategoryModel, ProductModel.category_id == CategoryModel.id)
        .join(ColourProduct, ProductModel.id == ColourProduct.product_id)
        .join(Promocode, ProductModel.promocode_id == Promocode.id)
        .options(joinedload(ProductModel.images))
        .filter(ProductModel.id == product_id)
        .first()
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
        price=query.price,
        visible=query.visible
    )

    result = MobileCharSchemaRead(
        id=model.id,
        product_id=[product_data],
        colour=model.colour,
        processor=model.processor,
        memory=model.memory,
        charger=model.charger,
        front_cam=model.front_cam,
        main_cam=model.main_cam,
        hrz=model.hrz,
        display=model.display,
        type_display=model.type_display,

    )

    return result



async def update_char_mobile(
        char_id: int,
        schema: MobileCharSchema,
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)
):
    # Получаем объект MobileChar по его ID
    mobile_char = db.query(MobileChar).filter(MobileChar.id == char_id).first()

    if not mobile_char:
        raise HTTPException(status_code=404, detail="MobileChar not found")

    # Обновляем данные из схемы
    mobile_char.colour = schema.colour
    mobile_char.processor = schema.processor
    mobile_char.memory = schema.memory
    mobile_char.charger = schema.charger
    mobile_char.front_cam = schema.front_cam
    mobile_char.main_cam = schema.main_cam
    mobile_char.hrz = schema.hrz
    mobile_char.display = schema.display
    mobile_char.type_display = schema.type_display

    db.commit()

    # Получаем данные о продукте и формируем результат для ответа
    product_data = db.query(ProductModel).get(mobile_char.product_id)
    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in product_data.images
    ]

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == product_data.category_id).first()

    colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == product_data.id).all()

    product_result = ProductSchemaReadV2(
        id=product_data.id,
        title=product_data.title,
        description=product_data.description,
        category=[CategorySchema(id=product_data.category_id, title=query_to_category.title)],
        images=images,
        owner=product_data.owner,
        created_at=product_data.created_at,
        count=product_data.count,
        procent_sale=product_data.procent_sale,
        promocode=[PromocodeReadSchema(id=product_data.promocode_rel.id,
                                       name=product_data.promocode_rel.name,
                                       procent=product_data.promocode_rel.procent,
                                       category=[product_data.promocode_rel.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                for colour in colour_data],
        price=product_data.price,
        visible=product_data.visible
    )

    result = MobileCharSchemaRead(
        id=mobile_char.id,
        product_id=[product_result],
        colour=mobile_char.colour,
        processor=mobile_char.processor,
        memory=mobile_char.memory,
        charger=mobile_char.charger,
        front_cam=mobile_char.front_cam,
        main_cam=mobile_char.main_cam,
        hrz=mobile_char.hrz,
        display=mobile_char.display,
        type_display=mobile_char.type_display,
    )

    return result



async def get_char_mobile(
        id: int,
        db: Session = Depends(get_db)
):
    # Получаем объект MobileChar по его ID
    mobile_char = db.query(MobileChar).filter(MobileChar.product_id == id).first()

    if not mobile_char:
        raise HTTPException(status_code=404, detail="MobileChar not found")

    # Получаем данные о продукте
    product_data = db.query(ProductModel).get(mobile_char.product_id)
    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in product_data.images
    ]

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == product_data.category_id).first()

    colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == product_data.id).all()

    product_result = ProductSchemaReadV2(
        id=product_data.id,
        title=product_data.title,
        description=product_data.description,
        category=[CategorySchema(id=product_data.category_id, title=query_to_category.title)],
        images=images,
        owner=product_data.owner,
        created_at=product_data.created_at,
        count=product_data.count,
        procent_sale=product_data.procent_sale,
        promocode=[PromocodeReadSchema(id=product_data.promocode_rel.id,
                                       name=product_data.promocode_rel.name,
                                       procent=product_data.promocode_rel.procent,
                                       category=[product_data.promocode_rel.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                for colour in colour_data],
        price=product_data.price,
        visible=product_data.visible
    )

    result = MobileCharSchemaRead(
        id=mobile_char.id,
        product_id=[product_result],
        colour=mobile_char.colour,
        processor=mobile_char.processor,
        memory=mobile_char.memory,
        charger=mobile_char.charger,
        front_cam=mobile_char.front_cam,
        main_cam=mobile_char.main_cam,
        hrz=mobile_char.hrz,
        display=mobile_char.display,
        type_display=mobile_char.type_display,
    )

    return result


async def get_all_mobile_char(
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)):
    query = db.query(MobileChar).all()

    return query



async def dlete_mobile_char(id: int,
                              db: Session = Depends(get_db),
                              login: dict = Depends(get_current_staff)):
    query = db.query(MobileChar).filter(MobileChar.id == id).first()

    if query is not None:
        query = db.query(MobileChar).filter(MobileChar.id == id).delete()

        db.commit()
        return JSONResponse(
            status_code=204,
            content={"message": "No Content"}
        )

    return HTTPException(
        status_code=404,
        detail="MobileChar not found"
    )


async def create_character_comp(schema: CompCharSchema,
                                product_id: int,
                                db: Session = Depends(get_db),
                                login: dict = Depends(get_current_staff)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    model = CompChar()
    model.colour = schema.colour
    model.product_id = product_id
    model.processor = schema.processor
    model.memory = schema.memory
    model.display = schema.display
    model.memory_type = schema.memory_type
    model.RAM = schema.RAM

    db.add(model)
    db.commit()

    query = (
        db.query(ProductModel)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .join(CategoryModel, ProductModel.category_id == CategoryModel.id)
        .join(ColourProduct, ProductModel.id == ColourProduct.product_id)
        .join(Promocode, ProductModel.promocode_id == Promocode.id)
        .options(joinedload(ProductModel.images))
        .filter(ProductModel.id == product_id)
        .first()
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
        price=query.price,
        visible=query.visible
    )

    result = CompCharSchemaRead(
        id=model.id,
        product_id=[product_data],
        colour=model.colour,
        processor=model.processor,
        memory=model.memory,
        display=model.display,
        memory_type=model.memory_type,
        RAM=model.RAM, )

    return result


async def get_character_comp(id: int, db: Session = Depends(get_db)):
    # Получаем данные о характеристиках компьютера по его ID
    comp_char = db.query(CompChar).filter(CompChar.product_id == id).first()

    if comp_char is None:
        raise HTTPException(status_code=404, detail="Computer Characteristic not found")

    product_data = db.query(ProductModel).get(comp_char.product_id)
    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in product_data.images
    ]

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == product_data.category_id).first()

    colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == product_data.id).all()

    product_result = ProductSchemaReadV2(
        id=product_data.id,
        title=product_data.title,
        description=product_data.description,
        category=[CategorySchema(id=product_data.category_id, title=query_to_category.title)],
        images=images,
        owner=product_data.owner,
        created_at=product_data.created_at,
        count=product_data.count,
        procent_sale=product_data.procent_sale,
        promocode=[PromocodeReadSchema(id=product_data.promocode_rel.id,
                                       name=product_data.promocode_rel.name,
                                       procent=product_data.promocode_rel.procent,
                                       category=[product_data.promocode_rel.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                for colour in colour_data],
        price=product_data.price,
        visible=product_data.visible
    )

    result = CompCharSchemaRead(
        id=comp_char.id,
        product_id=[product_result],
        colour=comp_char.colour,
        processor=comp_char.processor,
        memory=comp_char.memory,
        display=comp_char.display,
        memory_type=comp_char.memory_type,
        RAM=comp_char.RAM
    )

    return result


async def update_character_comp(
        char_id: int,
        schema: CompCharSchema,
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)
):
    # Получаем данные о характеристиках компьютера по его ID
    comp_char = db.query(CompChar).filter(CompChar.id == char_id).first()

    if comp_char is None:
        raise HTTPException(status_code=404, detail="Computer Characteristic not found")

    comp_char.colour = schema.colour
    comp_char.processor = schema.processor
    comp_char.memory = schema.memory
    comp_char.display = schema.display
    comp_char.memory_type = schema.memory_type
    comp_char.RAM = schema.RAM

    db.commit()

    product_data = db.query(ProductModel).get(comp_char.product_id)
    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in product_data.images
    ]

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == product_data.category_id).first()

    colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == product_data.id).all()

    product_result = ProductSchemaReadV2(
        id=product_data.id,
        title=product_data.title,
        description=product_data.description,
        category=[CategorySchema(id=product_data.category_id, title=query_to_category.title)],
        images=images,
        owner=product_data.owner,
        created_at=product_data.created_at,
        count=product_data.count,
        procent_sale=product_data.procent_sale,
        promocode=[PromocodeReadSchema(id=product_data.promocode_rel.id,
                                       name=product_data.promocode_rel.name,
                                       procent=product_data.promocode_rel.procent,
                                       category=[product_data.promocode_rel.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                for colour in colour_data],
        price=product_data.price,
        visible=product_data.visible
    )

    result = CompCharSchemaRead(
        id=comp_char.id,
        product_id=[product_result],
        colour=comp_char.colour,
        processor=comp_char.processor,
        memory=comp_char.memory,
        display=comp_char.display,
        memory_type=comp_char.memory_type,
        RAM=comp_char.RAM
    )

    return result


async def delete_comp_char(id: int,
                              db: Session = Depends(get_db),
                              login: dict = Depends(get_current_staff)):
    query = db.query(CompChar).filter(CompChar.id == id).first()

    if query is not None:
        query = db.query(CompChar).filter(CompChar.id == id).delete()

        db.commit()
        return JSONResponse(
            status_code=204,
            content={"message": "No Content"}
        )

    return HTTPException(
        status_code=404,
        detail="MobileChar not found"
    )


async def get_all_comp_char(
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)):
    query = db.query(CompChar).all()

    return query