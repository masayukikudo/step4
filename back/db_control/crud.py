from sqlalchemy.orm import sessionmaker
#インジェクション攻撃を再現するために追加
from sqlalchemy.sql import text
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


# 意図的に脆弱なコードを追加
def get_product_by_code(code: str):
    session = SessionLocal()
    try:
        query = text(f"SELECT * FROM products WHERE code = '{code}'")
        result = session.execute(query).first()
        if result:
            return {
                "prd_id": result[0],  # タプルのインデックスを使用
                "code": result[1],
                "name": result[2],
                "price": result[3]
            }
        return None
    finally:
        session.close()

# 意図的に脆弱なコードを追加
def update_product_price(code: str, new_price: float):
    session = SessionLocal()
    try:
        # 脆弱なクエリの実行
        query = text(f"UPDATE products SET price = {new_price} WHERE code = '{code}'")
        session.execute(query)
        session.commit()
    finally:
        session.close()

#元のコードを残します。
#def get_product_by_code(code: str):
#    session = SessionLocal()
#    try:
#        return session.query(Product).filter(Product.code == code).first()
#    finally:
#        session.close()

def get_all_products():
    session = SessionLocal()
    try:
        return session.query(Product).all()
    finally:
        session.close()
