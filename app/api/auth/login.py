from fastapi import Depends, HTTPException, status
from api.core.config import SECRET_KEY, AlGORITHM
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from api.models.admin_model import AdminModel
from api.auth.admin_auth import oauth2_bearer, for_user_exception, get_user_exceptions
from api.db.session import get_db
from api.models.user_model import UserModel

SECRET_KEY = SECRET_KEY
ALGORITHM = AlGORITHM


async def get_current_admin(token: str = Depends(oauth2_bearer),
                            db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")
    try:
        res = db.query(AdminModel).filter(AdminModel.gmail == gmail).first()

        is_super = res.is_superuser
        if res is None:
            raise for_user_exception()

        if is_super == False:
            raise for_user_exception()

        if gmail is None or user_id is None:
            raise get_user_exceptions()
    except AttributeError:
        raise for_user_exception()

    return {"sub": gmail, "user_id": user_id}


async def get_current_staff(token: str = Depends(oauth2_bearer),
                            db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(AdminModel).filter(AdminModel.gmail == gmail).first()

    if res is None:
        raise for_user_exception()

    is_staff = res.is_staff

    if is_staff == False:
        raise for_user_exception()

    if gmail is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}


async def get_current_user(token: str = Depends(oauth2_bearer),
                           db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(UserModel).filter(UserModel.gmail == gmail).first()


    if res is None:
        raise for_user_exception()

    if gmail is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}
