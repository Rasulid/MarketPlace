from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base

class CategoryModel(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    products = relationship("ProductModel", backref="category")
