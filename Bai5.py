from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

app = FastAPI(title="Hệ thống Quản lý Đơn hàng nâng cao")

orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"}
]

# HÀM BỔ TRỢ: Tạo cấu trúc Response chuẩn 6 trường 
# (statusCode, message, data, error, timestamp, path)

def make_standard_response(
    status_code: int, 
    message: str, 
    data: any = None, 
    error: any = None, 
    path: str = ""
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now().isoformat(),
        "path": path
    }


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors()
    message = "Dữ liệu gửi lên không đúng định dạng"
    
    response_body = make_standard_response(
        status_code=422,
        message=message,
        error=error_details,
        path=request.url.path
    )
    return JSONResponse(status_code=422, content=response_body)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    response_body = make_standard_response(
        status_code=exc.status_code,
        message=exc.detail,
        error="HTTP Business Error",
        path=request.url.path
    )
    return JSONResponse(status_code=exc.status_code, content=response_body)


@app.exception_handler(Exception)
def universal_exception_handler(request: Request, exc: Exception):
    response_body = make_standard_response(
        status_code=500,
        message="Hệ thống xảy ra sự cố bất ngờ ngoài danh mục xử lý",
        error=str(exc),
        path=request.url.path
    )
    return JSONResponse(status_code=500, content=response_body)


@app.delete("/orders/{order_id}")
def cancel_order(order_id: int, request: Request):
    
    # Bước 1: Tìm kiếm đơn hàng xem có tồn tại không
    target_order = None
    for o in orders_db:
        if o["id"] == order_id:
            target_order = o
            break
            
    if target_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found" 
        )
        
    if target_order["status"] == "DELIVERED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Hệ thống không cho phép hủy đơn hàng đã giao thành công"
        )
        
    target_order["status"] = "CANCELLED"
    
    success_response = make_standard_response(
        status_code=200,
        message="Hủy đơn hàng thành công",
        data=target_order,
        path=request.url.path
    )
    
    return success_response

@app.get("/orders")
def get_all_orders(request: Request):
    return make_standard_response(
        status_code=200,
        message="Lấy danh sách đơn hàng thành công",
        data=orders_db,
        path=request.url.path
    )