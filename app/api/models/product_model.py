
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base



class ProductModel(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='SET NULL'))
    owner = Column(Integer, ForeignKey('admins.id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=func.utcnow())
    count = Column(Integer)
    procent_sale = Column(Integer)
    promocode = Column(String)
    colour = Column(Integer, ForeignKey("colour.id", ondelete="SET NULL"))
    price = Column(Float)
    images = relationship("ProductImage", back_populates="product")

    category = relationship("CategoryModel", backref="products")
    colour = relationship("ColourModel", backref="products")

class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    product = relationship("ProductModel", back_populates="images")
