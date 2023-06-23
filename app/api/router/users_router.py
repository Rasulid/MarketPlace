from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from api.db.session import get_db
from api.schemas.users_schemas import User_Schema
from api.models.user_model import User_Model
from api.db.DataBasse import SessionLocal
from api.auth.admin_auth import password_hash, verify_password
from api.auth.login import get_user_exceptions, get_current_staff, get_current_user

router = FastAPI(title="Users")


@router.get("/user/{id}/", response_model=User_Schema)
async def list_users(id: int
                     , db: Session = Depends(get_db),
                     login: dict = Depends(get_current_user)):
    if login is None:
        return get_user_exceptions()

    query = db.query(User_Model).filter(User_Model.id == id).first()

    return query


@router.get("/users-list", response_model=List[User_Schema])
async def list_users(db: Session = Depends(get_db),
                     login: dict = Depends(get_current_staff)):
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
    user_model.is_superuser = False
    user_model.is_staff = False

    if user_model:
        user_name = db.query(User_Model).all()
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


@router.put("/update")
async def update_user(user: User_Schema,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_user)):
    id = login.get("user_id")
    user_model = db.query(User_Model) \
        .filter(User_Model.id == id).first()

    if user_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

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
    user_model.is_superuser = False
    user_model.is_staff = False

    check_admin = db.query(User_Model).filter(User_Model.gmail == login.get("sub")).first()

    if check_admin.id == user_model.id:
        hash_password = password_hash(user.password)
        user_model.password = hash_password
        db.add(user_model)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"Update admin {user_model.gmail} was successfully"})

    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"message": f"{user_model.gmail} is already exists"})


@router.put("/update/{id}")
async def update_user_by_id(user: User_Schema,
                            id:int,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_staff)):

    user_model = db.query(User_Model) \
        .filter(User_Model.id == id).first()

    if user_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

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
    user_model.is_superuser = False
    user_model.is_staff = False

    check_admin = db.query(User_Model).filter(User_Model.gmail == user_model.gmail).first()

    if check_admin.id == user_model.id:
        hash_password = password_hash(user.password)
        user_model.password = hash_password
        db.add(user_model)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"Update admin {user_model.gmail} was successfully"})

    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"message": f"{user_model.gmail} is already exists"})



@router.delete("/delete/{id}")
async def delete_user(db: Session = Depends(get_db),
                      login: dict = Depends(get_current_user)):
    id = login.get("user_id")

    query = db.query(User_Model).filter(User_Model.id == id).first()

    if query is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"})

    delete = db.query(User_Model).filter(User_Model.id == id).delete()

    db.commit()

    return delete


