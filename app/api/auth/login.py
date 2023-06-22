from fastapi import Depends, HTTPException, status
from api.core.config import SECRET_KEY, AlGORITHM
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from api.models.admin_model import Admin_Model
from api.auth.admin_auth import oauth2_bearer, for_user_exception, get_user_exceptions
from api.db.session import get_db
from models.user_model import User_Model

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
    res = db.query(Admin_Model).filter(Admin_Model.gmail == gmail).first()

    is_super = res.is_superuser
    if res is None:
        raise for_user_exception()

    if is_super == False:
        raise for_user_exception()

    if gmail is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}


async def get_current_staff(token: str = Depends(oauth2_bearer),
                            db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(Admin_Model).filter(Admin_Model.gmail == gmail).first()

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

    res = db.query(User_Model).filter(User_Model.gmail == gmail).first()

    print(res)

    if res is None:
        raise for_user_exception()

    if gmail is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}
