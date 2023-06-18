from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from api.db.session import get_db
from api.schemas.users_schemas import CreateUser, ReadUser
from api.models.user_model import User_Model
from api.db.DataBasse import SessionLocal
from api.auth.admin_auth import password_hash, verify_password

router = APIRouter(tags=["Users"],
                   prefix="/api/users")


# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

@router.get('api/users/list')
async def list_users(db:  Session = Depends(get_db)):
    return db.query(User_Model).all()

@router.post("/api/users/registr")
async def register(user: CreateUser,
                   db: Session = Depends(get_db)):
    user_model = User_Model()
    user_model.name = user.name
    user_model.email = user.email
    user_model.age = user.age
    user_model.is_superuser = user.is_superuser
    user_model.password = user.password
    user_model.is_verified = user.is_verified
    user_model.is_active = user.is_active
    user_model.is_staff = user.is_staff
    user_model.phone_number = user.phone_number
    user_model.country = user.country
    user_model.region = user.region
    user_model.is_user = True

    if user_model:
        user_name = db.query(User_Model).all()
        for x in user_name:
            if user_model.email == x.email or user_model.email == x.email:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail={'msg': f"{user_model.email} user is already exists"})
    hash_password = password_hash(user.password)
    user_model.password = hash_password

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": "User created successfully"})


@router.put("/api/users/update", response_model=ReadUser)
async def update(user: CreateUser, id: int,
                 db: Session = Depends(get_db)):
    user_model = db.query(User_Model) \
        .filter(User_Model.id == id).first()

    if user_model == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Admin not found"})

    user_model.name = user.name
    user_model.email = user.email
    user_model.age = user.age
    user_model.is_superuser = False
    user_model.password = user.password
    user_model.is_verified = True
    user_model.is_active = True
    user_model.is_staff = False
    user_model.phone_number = user.phone_number
    user_model.country = user.country
    user_model.region = user.region
    user_model.is_user = True

    hash_password = password_hash(user.password)
    user_model.password = hash_password

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "User updated successfully"})


@router.delete("api/users/delete")
async def delete(id: int,
                 db: Session = Depends(get_db)):
    admin_model = db.query(User_Model).filter(User_Model.id == id).first()

    if admin_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"})

    admin_model = db.query(User_Model).filter(User_Model.id == id).delete()

    db.commit()

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT   ,
        content={"message": "User deleted "})
