from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Column, DateTime, func
from api.db.DataBasse import Base


class User_Model(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    l_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    country = Column(String, default="UZB", nullable=False)
    region = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.utcnow())
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_user = Column(Boolean, default=True)
