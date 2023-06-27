from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, Float
from sqlalchemy.orm import relationship
from api.db.DataBasse import Base


class OrderedProduct(Base):
    __tablename__ = 'ordered_products'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"))
    count = Column(Integer)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    payment_method = Column(String)
    total_price = Column(Float)
    order_status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    ordered_products = relationship("OrderedProduct", secondary=OrderedProduct)
