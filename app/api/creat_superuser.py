from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.auth.admin_auth import password_hash
from api.db.session import get_db
from api.models.admin_model import AdminModel

router = FastAPI(title="SuperUser")

born_date = datetime(2003, 11, 30)


@router.post("/create/root/superuser")
async def register(db: Session = Depends(get_db)):
    admin_model = AdminModel()
    admin_model.name = "rasul"
    admin_model.born = born_date
    admin_model.created_at = datetime.now()
    admin_model.phone_number = "914774712"
    admin_model.gmail = "root@root.com"
    admin_model.password = "root"
    admin_model.country = "UZB"
    admin_model.region = "Tash"
    admin_model.is_active = True
    admin_model.is_staff = True
    admin_model.is_superuser = True
    admin_model.is_verified = True

    hash_password = password_hash('root')  # Make sure to implement this function correctly
    admin_model.password = hash_password

    user_name = db.query(AdminModel).all()
    for x in user_name:
        if admin_model.gmail == x.gmail:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user is already exists"
            )

    db.add(admin_model)
    db.commit()

    return "Success"
