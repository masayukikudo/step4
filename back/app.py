from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from db_control.crud import get_product_by_code, get_all_products, create_purchase, create_purchase_detail

app = FastAPI()

# CORS設定の追加
origins = [
    "https://localhost",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductModel(BaseModel):
    prd_id: Optional[int] = None
    code: str
    name: str
    price: float

class PurchaseModel(BaseModel):
    datetime: datetime
    emp_cd: str
    store_cd: str
    pos_no: str
    total_amount: float

class PurchaseDetailModel(BaseModel):
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int
    quantity: int

@app.get("/search_product/", response_model=ProductModel)
async def search_product(code: str) -> Optional[ProductModel]:
    product = get_product_by_code(code)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=List[ProductModel])
async def get_products() -> List[ProductModel]:
    products = get_all_products()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

#意図的に脆弱なコードを追加
@app.post("/update_price/")
async def update_price(code: str, new_price: float):
    logger.info(f"Updating price for product with code: {code} to {new_price}")
    try:
        update_product_price(code, new_price)
        return {"message": "Price updated successfully"}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/purchase/")
async def create_purchase_endpoint(purchase_details: List[PurchaseDetailModel]):
    total_amount = sum(detail.prd_price * detail.quantity for detail in purchase_details)
    purchase = PurchaseModel(
        datetime=datetime.now(),
        emp_cd="EMP001",
        store_cd="30",
        pos_no="90",
        total_amount=total_amount
    )
    created_purchase = create_purchase(
        datetime=purchase.datetime,
        emp_cd=purchase.emp_cd,
        store_cd=purchase.store_cd,
        pos_no=purchase.pos_no,
        total_amount=purchase.total_amount
    )
    print('Purchaseテーブルへの登録完了')
    for detail in purchase_details:
        create_purchase_detail(
            trd_id=created_purchase.trd_id,
            prd_id=detail.prd_id,
            prd_code=detail.prd_code,
            prd_name=detail.prd_name,
            prd_price=detail.prd_price,
            quantity=detail.quantity
        )
    return created_purchase
