from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base


class ColourModel(Base):
    __tablename__ = "colour"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    products = relationship("ProductModel", back_populates="colour")


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
    colour_id = Column(Integer, ForeignKey('colour.id', ondelete='SET NULL'))
    price = Column(Float)
    images = relationship("ProductImage", back_populates="product")

    category = relationship("CategoryModel", back_populates="products")
    colour = relationship("ColourModel", back_populates="products")


class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    product = relationship("ProductModel", back_populates="images")


"""
backref и back_populates - это два разных параметра, используемых для определения обратных отношений между моделями в SQLAlchemy.

backref: Этот параметр определяет автоматическое создание обратной ссылки на связанный объект. Когда вы используете backref, SQLAlchemy автоматически создает новое свойство в связанной модели, которое обеспечивает доступ к родительскому объекту или коллекции объектов.

back_populates: Этот параметр позволяет явно указать имя свойства в связанной модели, которое будет использоваться в качестве обратной ссылки. Вместо того, чтобы SQLAlchemy автоматически создавал новое свойство, вы указываете существующее свойство в связанной модели, которое должно быть использовано в качестве обратной ссылки.

Использование back_populates предпочтительно, когда у вас уже есть существующее свойство в модели, и вы хотите явно указать его в качестве обратной ссылки. Это позволяет предотвратить конфликты и уточняет намерения вашего кода.

В целом, backref и back_populates предоставляют схожую функциональность, но с разным уровнем явности в определении обратных ссылок. Выбор между ними зависит от ваших предпочтений и требований вашего проекта.
"""