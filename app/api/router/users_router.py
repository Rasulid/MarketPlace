from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from api.db.session import get_db
from api.schemas.users_schemas import CreateUser, ReadUser
from api.models.user_model import User_Model
from api.db.DataBasse import SessionLocal
from api.auth.admin_auth import password_hash, verify_password
from api.auth.login import get_current_staff, get_user_exceptions

router = APIRouter(tags=["Users"],
                   prefix="/api/users")


@router.get("/list-users")
async def list_users(db: Session = Depends(get_db),
                     login: dict = Depends(get_current_staff)):
    if login is None:
        return get_user_exceptions()

    query = db.query(User_Model).all()

    return query
