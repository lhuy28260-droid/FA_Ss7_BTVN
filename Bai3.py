from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Hệ thống Xử lý Đơn hàng Ecommerce (Phong cách Cổ điển)")

class OrderRequestModel(BaseModel):
    product_id: int
    quantity: int


products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]

orders_db = []

@app.get("/products")
def get_products():
    return products_db

@app.get("/orders")
def get_orders():
    return orders_db

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderRequestModel):
    
    if payload.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Số lượng mua phải lớn hơn 0"
        )
        
    target_product = None
    for p in products_db:
        if p["id"] == payload.product_id:
            target_product = p
            break
            
    if target_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Sản phẩm không tồn tại trên hệ thống"
        )
        
    if payload.quantity > target_product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Sản phẩm không đủ số lượng trong kho"
        )
        
    
    
    target_product["stock"] = target_product["stock"] - payload.quantity
    
    
    total_price = target_product["price"] * payload.quantity
    
   
    new_order_id = 1
    if orders_db:
        max_id = orders_db[0]["id"]
        for o in orders_db:
            if o["id"] > max_id:
                max_id = o["id"]
        new_order_id = max_id + 1
        
    
    new_order = {
        "id": new_order_id,
        "product_id": payload.product_id,
        "product_name": target_product["name"],
        "quantity": payload.quantity,
        "total_price": total_price
    }
    
    
    orders_db.append(new_order)
    
    
    return {
        "message": "Tạo đơn hàng thành công", 
        "order_details": new_order
    }