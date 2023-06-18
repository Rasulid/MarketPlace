from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.models.user_model import User_Model
from api.db.DataBasse import SessionLocal
from api.schemas.users_schemas import CreateUser, ReadUser
from api.db.session import get_db

router = APIRouter(tags=["Admin"],
                   prefix="/api/admin")

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


@router.put("/update", response_model=ReadUser)
async def update_admin(id: int, admin: CreateUser,
                       db: Session = Depends(get_db)):
    admin_model = db.query(User_Model)\
        .filter(User_Model.id == id).first()

    if admin_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})


    admin_model.name = admin.name
    admin_model.email = admin.email
    admin_model.age = admin.age
    admin_model.is_superuser = admin.is_superuser
    admin_model.password = admin.password
    admin_model.is_verified = admin.is_verified
    admin_model.is_active = admin.is_active
    admin_model.is_staff = admin.is_staff
    admin_model.phone_number = admin.phone_number
    admin_model.country = admin.country
    admin_model.region = admin.region
    admin_model.is_user = False

    db.add(admin_model)
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Update admin successfully"})


@router.delete("/delete")
async def delete_admin(id: int,
                       db: Session = Depends(get_db)):
    db_query = db.query(User_Model)\
        .filter(User_Model.id == id).first()

    if db_query is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

    db_query = db.query(User_Model).filter(User_Model.id == id).delete()
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                        content={"message": "delete admin successfully"})

