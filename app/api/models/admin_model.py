from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Column, DateTime, func
from api.db.DataBasse import Base

class Admin_Model(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.utcnow())
    phone_number = Column(String, nullable=False)
    gmail = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    country = Column(String, default="UZB")
    region = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)



