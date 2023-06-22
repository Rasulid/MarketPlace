from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from api.db.session import get_db
from api.schemas.users_schemas import User_Schema
from api.models.user_model import User_Model
from api.db.DataBasse import SessionLocal
from api.auth.admin_auth import password_hash, verify_password
from api.auth.login import get_user_exceptions, get_current_staff, get_current_user

router = APIRouter(tags=["Users"],
                   prefix="/api/users")


@router.get("/list-users")
async def list_users(db: Session = Depends(get_db),
                     login: dict = Depends(get_current_user)):
    if login is None:
        return get_user_exceptions()

    query = db.query(User_Model).all()

    return query


@router.post("/register", response_model=List[User_Schema])
async def register(user: User_Schema,
                   db: Session = Depends(get_db)):
    res = []

    user_model = User_Model()
    user_model.name = user.name
    user_model.l_name = user.l_name
    user_model.age = user.age
    user_model.phone_number = user.phone_number
    user_model.country = user.country
    user_model.region = user.region
    user_model.gmail = user.gmail
    user_model.password = user.password
    user_model.created_at = user.created_at
    user_model.is_active = user.is_active
    user_model.is_verified = user.is_verified
    user_model.update_at = user.update_at

    res.append(user_model)

    db.add(user_model)
    db.commit()

    return res
