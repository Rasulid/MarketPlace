from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from api.db.session import get_db
from api.schemas.users_schemas import UserSchema, UserSchemaRead, CreateUserSchema
from api.models.user_model import UserModel
from api.auth.admin_auth import password_hash
from api.auth.login import get_user_exceptions, get_current_staff, get_current_user
from api.core.config import SECRET_KEY
from api.models.admin_model import AdminModel

router = APIRouter()


async def lists_users(id: int
                      , db: Session = Depends(get_db),
                      login: dict = Depends(get_current_user)):
    if login is None:
        return get_user_exceptions()

    query = db.query(UserModel).filter(UserModel.id == id).first()
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user Not Found"
        )

    return query


async def user(db: Session = Depends(get_db),
               login: dict = Depends(get_current_user)):
    id = login.get("user_id")
    if login is None:
        return get_user_exceptions()

    query = db.query(UserModel).filter(UserModel.id == id).first()
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user Not Found"
        )

    return query


async def list_users(db: Session = Depends(get_db),
                     login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    query = db.query(UserModel).all()

    return query


async def me(token: str,
             db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
        query = db.query(UserModel).filter(UserModel.id == user_id).first()

        if query is None:
            query = db.query(AdminModel).filter(AdminModel.id == user_id).first()

        return query
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def register(user: CreateUserSchema,
                   db: Session = Depends(get_db)):
    res = []

    user_model = UserModel()
    user_model.name = user.name
    user_model.l_name = user.l_name
    user_model.born = user.born
    user_model.phone_number = user.phone_number
    user_model.country = user.country
    user_model.region = user.region
    user_model.gmail = user.gmail
    user_model.password = user.password
    user_model.created_at = datetime.utcnow()
    user_model.is_active = True
    user_model.is_verified = True
    user_model.update_at = datetime.utcnow()
    user_model.is_superuser = False
    user_model.is_staff = False

    if user_model:
        user_name = db.query(UserModel).all()
        for x in user_name:
            if user_model.gmail == x.gmail:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail={'msg': f"{user_model.gmail} user is already exists"})
    hash_password = password_hash(user.password)
    user_model.password = hash_password

    res.append(user_model)

    db.add(user_model)
    db.commit()

    return res


async def update_user_by_id(user: CreateUserSchema,
                            id: int,
                            db: Session = Depends(get_db),
                            login: dict = Depends(get_current_staff)):
    user_model = db.query(UserModel) \
        .filter(UserModel.id == id).first()

    if user_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

    user_model.name = user.name
    user_model.l_name = user.l_name
    user_model.born = user.born
    user_model.phone_number = user.phone_number
    user_model.country = user.country
    user_model.region = user.region
    user_model.gmail = user.gmail
    user_model.password = user.password
    user_model.created_at = datetime.utcnow()
    user_model.is_active = True
    user_model.is_verified = True
    user_model.update_at = datetime.utcnow()
    user_model.is_superuser = False
    user_model.is_staff = False

    check_admin = db.query(UserModel).filter(UserModel.gmail == user_model.gmail).first()

    if check_admin.id == user_model.id:
        hash_password = password_hash(user.password)
        user_model.password = hash_password
        db.add(user_model)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"Update admin {user_model.gmail} was successfully"})

    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"message": f"{user_model.gmail} is already exists"})


async def user_update(user: CreateUserSchema,
                      db: Session = Depends(get_db),
                      login: dict = Depends(get_current_staff)):
    id = login.get('user.id')

    user_model = db.query(UserModel) \
        .filter(UserModel.id == id).first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")

    user_model.name = user.name
    user_model.l_name = user.l_name
    user_model.born = user.born
    user_model.phone_number = user.phone_number
    user_model.country = user.country
    user_model.region = user.region
    user_model.gmail = user.gmail
    user_model.password = user.password
    user_model.created_at = datetime.utcnow()
    user_model.is_active = True
    user_model.is_verified = True
    user_model.update_at = datetime.utcnow()
    user_model.is_superuser = False
    user_model.is_staff = False

    check_admin = db.query(UserModel).filter(UserModel.gmail == user_model.gmail).first()

    if check_admin.id == user_model.id:
        hash_password = password_hash(user.password)
        user_model.password = hash_password
        db.add(user_model)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"Update admin {user_model.gmail} was successfully"})

    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"message": f"{user_model.gmail} is already exists"})


async def delete_user(id: int,
                      db: Session = Depends(get_db),
                      login: dict = Depends(get_current_user)):
    query = db.query(UserModel).filter(UserModel.id == id).first()

    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")

    delete = db.query(UserModel).filter(UserModel.id == id).delete()

    db.commit()

    return delete
