from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from api.db.DataBasse import Base


class ColourModel(Base):
    __tablename__ = "colour"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    products = relationship("ProductModel", backref="colour")
