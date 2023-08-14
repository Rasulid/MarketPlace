from sqlalchemy import  Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from api.db.DataBasse import Base


class MobileChar(Base):
    __tablename__ ='mobile_char'
    id = Column(Integer,primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    colour = Column(String)
    processor = Column(String)
    memory = Column(String)
    charger = Column(String)
    front_cam = Column(String)
    main_cam = Column(String)
    hrz = Column(String)
    display = Column(String)
    type_display = Column(String)

    product_rel = relationship("ProductModel", back_populates='mobile_char')


class CompChar(Base):
    __tablename__ = 'comp_char'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    colour = Column(String)
    processor = Column(String)
    memory = Column(String)
    display = Column(String)
    memory_type = Column(String)
    RAM = Column(String)

    product_rel = relationship("ProductModel", back_populates='comp_char')
