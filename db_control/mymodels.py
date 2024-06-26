from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timezone

Base = declarative_base()
main_path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir(main_path)
engine = create_engine('sqlite:///Commerce.db', echo=True)
Session = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'Products'

    prd_id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.prd_id}>'

class Purchase(Base):
    __tablename__ = 'Purchases'

    trd_id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    emp_cd = Column(String)
    store_cd = Column(String)
    pos_no = Column(String)
    total_amount = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Purchase {self.id}>'

class PurchaseDetail(Base):
    __tablename__ = "Purchase_details"

    dtl_id = Column(Integer, primary_key=True, index=True)
    trd_id = Column(Integer, ForeignKey("Purchases.trd_id"))
    prd_id = Column(Integer, ForeignKey("Products.prd_id"))
    prd_code = Column(String)
    prd_name = Column(String)
    prd_price = Column(Integer)
    quantity = Column(Integer)



