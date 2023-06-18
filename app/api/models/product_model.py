
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime, func
from api.db.DataBasse import Base


class Product_Model(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    category = Column(String, nullable=False)
    photos = Column(String, nullable=False)
    owner = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"))  # FK to Admin relationship one to many
    created_at = Column(DateTime, default=func.utcnow())
    count = Column(Integer, nullable=False)
    procent_sale = Column(Integer)
    promocode = Column(String)
    colour = Column(String, nullable=False)
