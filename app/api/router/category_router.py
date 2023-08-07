from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import CategoryModel, ProductModel
from api.auth.login import get_current_staff
from api.schemas.product_schema import ProductSchemaSearch, ProductImageSchema

router = APIRouter(
    tags=["Category"],
    prefix="/api/category"
)


async def category_by_id(id: int,
                         db: Session = Depends(get_db),
                         login: dict = Depends(get_current_staff)):
    query = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    return query


async def category_list(db: Session = Depends(get_db),
                        login: dict = Depends(get_current_staff)
                        ):
    query = db.query(CategoryModel).all()
    return query


class CategoryCreate(BaseModel):
    title: str


async def category_create(
        title: CategoryCreate,
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)
):
    model = CategoryModel()
    model.title = title.title

    title = title.title

    query = db.query(CategoryModel).filter(CategoryModel.title == title).first()
    print(query)
    if query is None:
        db.add(model)
        db.commit()

        return model
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content="this colour already exists")


async def category_update(id: int,
                          title: CategoryCreate,
                          db: Session = Depends(get_db),
                          login: dict = Depends(get_current_staff)
                          ):
    query = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if query is not None:
        query.title = title.title

        db.add(query)
        db.commit()

        return query
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="category not found"
    )


async def delete_category(id: int,
                          db: Session = Depends(get_db),
                          login: dict = Depends(get_current_staff)
                          ):
    chack = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if chack is not None:
        delete = db.query(CategoryModel).filter(CategoryModel.id == id).delete()

        db.commit()

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content="Category deleted successfully"
        )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Category not found"
    )

async def category_by_product(id: int, db: Session = Depends(get_db)):
    result = []
    query = db.query(ProductModel).filter(ProductModel.category_id == id).all()
    for x in query:
        images = [
            ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
            for image in x.images
        ]
        res = ProductSchemaSearch(
            id=x.id,
            title=x.title,
            images=images,
            price=x.price,
        )
        result.append(res)

    return result
