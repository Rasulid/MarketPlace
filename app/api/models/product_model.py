from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base


class ColourProduct(Base):
    __tablename__ = 'colour_product'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    colour_id = Column(Integer, ForeignKey("colour.id", ondelete="SET NULL"))


class ColourModel(Base):
    __tablename__ = "colour"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    # products = relationship("ProductModel", back_populates="colour")
    colour_products = relationship("ColourProduct", secondary="colour_product",
                                   primaryjoin="ColourModel.id == ColourProduct.colour_id",
                                   secondaryjoin="ColourModel.id == ColourProduct.colour_id")


class CategoryModel(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    products = relationship("ProductModel", back_populates="category")


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
    promocode = Column(String)
    price = Column(Float)
    images = relationship("ProductImage", back_populates="product")

    category = relationship("CategoryModel", back_populates="products")
    # colour_products = relationship("ColourProduct", back_populates="product_model")


class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    product = relationship("ProductModel", back_populates="images")