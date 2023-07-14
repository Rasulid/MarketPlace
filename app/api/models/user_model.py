from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Column, DateTime, func
from api.db.DataBasse import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    l_name = Column(String, nullable=False)
    born = Column(DateTime, nullable=True)
    phone_number = Column(String, nullable=False)
    country = Column(String, default="UZB", nullable=False)
    region = Column(String, nullable=False)
    gmail = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.utcnow())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    update_at = Column(DateTime, default=func.utcnow())



# Base.metadata.remove(User_Model.__table__)
#
# # Создать определение таблицы 'users' заново
# Base.metadata.create_all(engine)