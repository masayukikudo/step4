import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mymodels import Base, Product

# 現在のディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# データベースの設定
engine = create_engine('sqlite:///Commerce.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# サンプルデータの作成
products = [
    {"prd_id":"1","code": "000001", "name": "お茶", "price": 150},
    {"prd_id":"2","code": "000002", "name": "コーラ", "price": 200},
    {"prd_id":"3","code": "000003", "name": "水", "price": 100},
    # 追加したい他のデータをここに記入
]

# データをProductsテーブルに挿入
for product_data in products:
    product = Product(**product_data)
    session.add(product)

session.commit()
session.close()

print("Products have been added to the database.")
