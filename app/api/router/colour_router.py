from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.session import get_db
from api.models.product_model import ColourModel
from api.schemas.colour_schema import ColourSchema
from api.auth.login import get_current_staff

router = APIRouter(
    tags=["Colour"],
    prefix="/api/colour"
)


async def list_colours(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    query = db.query(ColourModel).all()
    return query


async def colour_by_id(id: int,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    query = db.query(ColourModel).filter(ColourModel.id == id).first()
    return query


class ColourCreate(BaseModel):
    title: str


async def colour_create(
        title: ColourCreate,
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)
):
    model = ColourModel()
    model.title = title.title

    title = title.title

    query = db.query(ColourModel).filter(ColourModel.title == title).first()
    if query is None:
        db.add(model)
        db.commit()

        return model
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content="this colour already exists")


async def colour_update(id: int,
                        title: ColourCreate,
                        db: Session = Depends(get_db),
                        login: dict = Depends(get_current_staff)
                        ):
    query = db.query(ColourModel).filter(ColourModel.id == id).first()

    if query is not None:
        query.title = title.title

        db.add(query)
        db.commit()

        return query
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Colour not found"
    )


async def delete_colour(id: int,
                        db: Session = Depends(get_db),
                        login: dict = Depends(get_current_staff)
                        ):
    chack = db.query(ColourModel).filter(ColourModel.id == id).first()

    if chack is not None:
        delete = db.query(ColourModel).filter(ColourModel.id == id).delete()

        db.commit()

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content="Colour deleted successfully"
        )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Colour not found"
    )
