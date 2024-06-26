from sqlalchemy.orm import sessionmaker
from .mymodels import Purchase, Product, PurchaseDetail, engine

# セッションの作成
SessionLocal = sessionmaker(bind=engine)

def create_purchase(datetime, emp_cd, store_cd, pos_no, total_amount):
    session = SessionLocal()
    try:
        purchase = Purchase(
            datetime = datetime,
            emp_cd = emp_cd,
            store_cd = store_cd,
            pos_no = pos_no,
            total_amount = total_amount
        )
        session.add(purchase)
        session.commit()
        session.refresh(purchase)
        return purchase
    finally:
        session.close()

def create_purchase_detail(trd_id, prd_id, prd_code, prd_name, prd_price, quantity):
    session = SessionLocal()
    try:
        purchase_detail = PurchaseDetail(
            trd_id = trd_id,
            prd_id = prd_id,
            prd_code = prd_code,
            prd_name = prd_name,
            prd_price = prd_price,
            quantity = quantity
        )
        session.add(purchase_detail)
        session.commit()
        session.refresh(purchase_detail)
        return purchase_detail
    finally:
        session.close()

def get_product_by_code(code: str):
    session = SessionLocal()
    try:
        return session.query(Product).filter(Product.code == code).first()
    finally:
        session.close()

def get_all_products():
    session = SessionLocal()
    try:
        return session.query(Product).all()
    finally:
        session.close()
