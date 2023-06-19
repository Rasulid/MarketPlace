from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.auth.admin_auth import password_hash
from api.db.session import get_db
from api.models.admin_model import Admin_Model

app = FastAPI()


@app.post("/api/create/root/superuser")
def register(db: Session = Depends(get_db)):
    admin_model = Admin_Model()
    admin_model.name = "rasul"
    admin_model.age = 20
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

    hash_password = password_hash('root')
    admin_model.password = hash_password

    if admin_model:
        user_name = db.query(Admin_Model).all()
        for x in user_name:
            if admin_model.gmail == x.gmail:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail={'msg': "user is already exists"})

    db.add(admin_model)
    db.commit()

    return "Success"
