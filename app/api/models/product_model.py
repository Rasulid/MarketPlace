
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base


class Product_Model(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    category = Column(String, nullable=False)
    owner = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"))  # FK to Admin relationship one to many
    created_at = Column(DateTime, default=func.utcnow())
    count = Column(Integer, nullable=False)
    procent_sale = Column(Integer)
    promocode = Column(String)
    colour = Column(String, nullable=False)

    images = relationship("Product_Image", back_populates="product")


class Product_Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"))

    product = relationship("Product_Model", back_populates="images")