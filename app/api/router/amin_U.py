from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models.user_model import User_Model
from api.db.DataBasse import SessionLocal
from api.schemas.users_schemas import CreateUser, ReadUser


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter(tags=["Admin"],
                   prefix="/api/admin")


@router.post('/create')
async def create_admin(admin: CreateUser,
                       db: Session = Depends(get_db)):
    admin_model = User_Model()

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

    db.add(admin_model)
    db.commit()

    return admin_model


@router.get('/list')
async def list_admin(db: Session = Depends(get_db)):
    res = db.query(User_Model).all()
    print(res)
    return res


