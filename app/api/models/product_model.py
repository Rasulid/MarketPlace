
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base



class ProductModel(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=func.utcnow())
    count = Column(Integer, nullable=False)
    percent_sale = Column(Integer)
    promocode = Column(String)
    color = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    images = relationship("ProductImage", back_populates="product")


class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    product = relationship("ProductModel", back_populates="images")
