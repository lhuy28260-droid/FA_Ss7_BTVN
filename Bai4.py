from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Hệ thống Tra cứu Thanh toán Chuẩn Bảo mật")

orders_list = [
    {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"}
]

orders_dict = {}
for order in orders_list:
    order_id = order["id"]
    orders_dict[order_id] = order

@app.get("/orders/{order_id}/payment")
def get_payment_history(order_id: int):
    
    try:

        if order_id not in orders_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
            
        target_order = orders_dict[order_id]
        
        return {
            "order_id": target_order["id"],
            "payment_status": target_order["payment_status"],
            "method": target_order["method"]
        }

    except HTTPException as http_error:
        raise http_error
        
    except Exception as raw_error:
        
        print(f"[SERVER LOG LỖI]: {str(raw_error)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Hệ thống đang gặp sự cố xử lý kỹ thuật, vui lòng quay lại sau."
        )