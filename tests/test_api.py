from fastapi.testclient import TestClient
import sys
import os

# ルートディレクトリをシステムパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


client = TestClient(app)

'''
def test_search_product():
    # テスト用の商品コードを指定（実際にデータベースに存在するものである必要があります）
    response = client.get(
        f"/search_product/?code=000001"
    )
    assert response.status_code == 200
    # ここでは具体的なレスポンスの形式に基づいて検証を行う
    assert response.json() == {
        'prd_id': 1,
        "code": '000001',
        "name": "お茶",
        "price": 150.0
    }

if __name__ == "__main__":
    test_search_product()

'''

# 無効化しています。無効化を辞める場合はdisable_を削除
def disable_test_create_purchase():
    response = client.post(
        "/purchase/",
        json=[
            {
                "prd_id": 1,
                "prd_code": "000001",
                "prd_name": "お茶",
                "prd_price": 150,
                "quantity": 2
            },
            {
                "prd_id": 2,
                "prd_code": "000002",
                "prd_name": "コーラ",
                "prd_price": 200,
                "quantity": 1
            }
        ]
    )
    print(response.json())
    assert response.status_code == 200
    


