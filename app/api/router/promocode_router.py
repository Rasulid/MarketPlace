from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.product_model import Promocode
from api.schemas.promocode_schema import PromocodeSchema, PromocodeReadSchema
from api.auth.login import get_current_staff

router = APIRouter(tags=["Promocode"],
                   prefix="/api/promocode")


@router.get("/get-list-prom")
async def create_promocode(db: Session = Depends(get_db),
                           login: dict = Depends(get_current_staff)
                           ):
    query = db.query(Promocode).all()
    return query


@router.post("/create", response_model=PromocodeReadSchema)
async def create_promocode(promocode_schemas: PromocodeSchema,
                           db: Session = Depends(get_db),
                           login: dict = Depends(get_current_staff)):
    res = []

    promocode_model = Promocode()
    promocode_model.name = promocode_schemas.name
    promocode_model.procent = promocode_schemas.procent

    res.append(promocode_model)
    db.add(promocode_model)
    db.commit()

    return promocode_model


@router.put("/update/{id}", response_model=PromocodeReadSchema)
async def update_promocode(id: int,
                           promocode_schemas: PromocodeSchema,
                           db: Session = Depends(get_db),
                           login: dict = Depends(get_current_staff)):
    query = db.query(Promocode).filter(Promocode.id == id).first()

    if query is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Promocode not found")

    query.name = promocode_schemas.name
    query.procent = promocode_schemas.procent

    db.add(query)
    db.commit()

    return query


@router.delete("/delete/{id}")
async def delete_promocode(id: int,
                           db: Session = Depends(get_db),
                           login: dict = Depends(get_current_staff)):
    query = db.query(Promocode).filter(Promocode.id == id).first()

    if query is not None:
        delete = db.query(Promocode).filter(Promocode.id == id).delete()

        db.commit()

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content="Deleted"
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Promocode not found")


@router.get("/get-by/{id}", response_model=PromocodeReadSchema)
async def get_promocode_by_id(id: int,
                           db: Session = Depends(get_db),
                              login: dict = Depends(get_current_staff)):
    query = db.query(Promocode).filter(Promocode.id == id).first()

    if query is not None:
        return query

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Promocode not found")
