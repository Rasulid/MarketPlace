from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.db.session import get_db
from api.models.product_model import ColourModel
from api.schemas.colour_schema import ColourSchema
from api.auth.login import get_current_staff

router = APIRouter(
    tags=["Colour"],
    prefix="/api/colour"
)


@router.get("/")
async def list_colours(db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):
    query = db.query(ColourModel).all()
    return query


@router.post("/create", response_model=ColourSchema)
async def category_create(
        title: str,
        db: Session = Depends(get_db),
        login: dict = Depends(get_current_staff)
):
    model = ColourModel()
    model.title = title

    query = db.query(ColourModel).filter(ColourModel.title == title).first()
    if query is None:
        db.add(model)
        db.commit()

        return model
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content="this colour already exists")


@router.put("/update/{id}}", response_model=ColourSchema)
async def category_update(id: int,
                          title: str,
                          db: Session = Depends(get_db),
                          login: dict = Depends(get_current_staff)
                          ):
    query = db.query(ColourModel).filter(ColourModel.id == id).first()

    if query is not None:
        query.title = title

        db.add(query)
        db.commit()

        return query
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Colour not found"
    )


@router.delete("/delete/{id}")
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
