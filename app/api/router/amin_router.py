from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.db.session import get_db
from api.auth.admin_auth import password_hash
from api.auth.login import get_current_admin, get_user_exceptions
from api.schemas.admin_schema import Admin_Schema, Admin_Read_Schema
from api.models.admin_model import AdminModel

router = APIRouter()


async def register(admin: Admin_Schema,
                   db: Session = Depends(get_db),
                   login: dict = Depends(get_current_admin)):
    res = []

    admin_model = AdminModel()
    admin_model.name = admin.name
    admin_model.age = admin.age
    admin_model.created_at = admin.created_at
    admin_model.phone_number = admin.phone_number
    admin_model.gmail = admin.gmail
    admin_model.password = admin.password
    admin_model.country = admin.country
    admin_model.region = admin.region
    admin_model.is_active = admin.is_active
    admin_model.is_staff = admin.is_staff
    admin_model.is_superuser = admin.is_superuser
    admin_model.is_verified = admin.is_verified

    if admin_model:
        user_name = db.query(AdminModel).all()
        for x in user_name:
            if admin_model.gmail == x.gmail:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail={'msg': f"{admin_model.gmail} user is already exists"})
    hash_password = password_hash(admin.password)
    admin_model.password = hash_password

    res.append(admin_model)

    db.add(admin_model)
    db.commit()

    return res


async def update_admin(admin: Admin_Schema,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_admin)):
    id = login.get("user_id")
    admin_model = db.query(AdminModel) \
        .filter(AdminModel.id == id).first()

    if admin_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

    admin_model.name = admin.name
    admin_model.age = admin.age
    admin_model.created_at = admin.created_at
    admin_model.phone_number = admin.phone_number
    admin_model.gmail = admin.gmail
    admin_model.password = admin.password
    admin_model.country = admin.country
    admin_model.region = admin.region
    admin_model.is_active = admin.is_active
    admin_model.is_staff = admin.is_staff
    admin_model.is_superuser = admin.is_superuser
    admin_model.is_verified = admin.is_verified

    check_admin = db.query(AdminModel).filter(AdminModel.gmail == login.get("sub")).first()

    if check_admin.id == admin_model.id:
        hash_password = password_hash(admin.password)
        admin_model.password = hash_password
        db.add(admin_model)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"Update admin {admin_model.gmail} was successfully"})

    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"message": f"{admin_model.gmail} is already exists"})


async def user_list(db: Session = Depends(get_db),
                    user: dict = Depends(get_current_admin)):
    if user is None:
        raise get_user_exceptions()

    model_ = db.query(AdminModel).all()
    return model_


async def delete_admin(id: int,
                        db: Session = Depends(get_db),
                       login: dict = Depends(get_current_admin)):

    db_query = db.query(AdminModel) \
        .filter(AdminModel.id == id).first()

    if db_query is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

    delete = db.query(AdminModel).filter(AdminModel.id == id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
