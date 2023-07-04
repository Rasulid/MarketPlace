from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import CategoryModel
from api.schemas.category_schema import CategorySchema
from api.auth.login import get_current_staff

router = APIRouter(
    tags=["Category"],
    prefix="/api/category"
)


@router.get('/')
async def category_list(db: Session = Depends(get_db),
                        login: dict = Depends(get_current_staff)
                        ):
    query = db.query(CategoryModel).all()
    return query


@router.post("/create", response_model=CategorySchema)
async def category_create(
        title: str,
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)
):
    model = CategoryModel()
    model.title = title

    query = db.query(CategoryModel).filter(CategoryModel.title == title).first()
    print(query)
    if query is None:

        db.add(model)
        db.commit()

        return model
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content="this colour already exists")


@router.put("/update/{id}}", response_model=CategorySchema)
async def category_update(id: int,
                          title: str,
                          db: Session = Depends(get_db),
                          login: dict = Depends(get_current_staff)
                          ):
    query = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if query is not None:
        query.title = title

        db.add(query)
        db.commit()

        return query
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="category not found"
    )



@router.delete("/delete/{id}")
async def delete_colour(id: int,
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