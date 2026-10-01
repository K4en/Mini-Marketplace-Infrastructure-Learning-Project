from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int


class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    created_at: datetime

class ShipmentResponse(BaseModel):
    id: int
    order_id: int
    status: str
    created_at: datetime