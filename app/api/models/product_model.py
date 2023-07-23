from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base


class Promocode(Base):
    __tablename__ = "promocode"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    procent = Column(Integer)
    category = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=True)

    category_rel = relationship("CategoryModel", back_populates="promocode")
    product_rel = relationship("ProductModel", back_populates='promocode_rel')
    order_rel = relationship("Order", back_populates='promocode_rel')


class ColourProduct(Base):
    __tablename__ = 'colour_product'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    colour_id = Column(Integer, ForeignKey("colour.id", ondelete="CASCADE"))


class ColourModel(Base):
    __tablename__ = "colour"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class CategoryModel(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    promocode = relationship("Promocode", back_populates='category_rel')
    products_rel = relationship("ProductModel", back_populates="category_rel")


class ProductModel(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='SET NULL'))
    owner = Column(Integer, ForeignKey('admins.id', ondelete='SET NULL'))
    created_at = Column(DateTime)
    count = Column(Integer)
    procent_sale = Column(Integer)
    promocode_id = Column(Integer, ForeignKey('promocode.id', ondelete='SET NULL'))
    price = Column(Float)
    visible = Column(Boolean)

    images = relationship("ProductImage", back_populates="product")
    category_rel = relationship("CategoryModel", back_populates="products_rel")
    colour_products_rel = relationship("ColourProduct", backref="product")
    promocode_rel = relationship("Promocode", back_populates="product_rel")


class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    product = relationship("ProductModel", back_populates="images")
