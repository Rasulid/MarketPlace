from uuid import uuid4
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from api.db.DataBasse import Base


class Order_Model(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_payment = Column(String)
    ordered_price = Column(Integer)
    ordered_products = relationship("OrderedProduct_Model", backref="orders")
    prod_img = Column(String)
    order_status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))


class OrderedProduct_Model(Base):
    __tablename__ = 'ordered_products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"))
