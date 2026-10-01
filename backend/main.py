from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
import sqlite3
from datetime import datetime, timedelta
from starlette.middleware.cors import CORSMiddleware
from kafka import KafkaProducer
import json


from models import (
    ProductCreate,
    OrderCreate,
    ProductResponse,
    OrderResponse,
    ShipmentResponse
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

producer = KafkaProducer(bootstrap_servers=["kafka:9093"],)

@app.get("/products", response_model=list[ProductResponse])
def get_products():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return [
        {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "stock": product[3],
        }
        for product in products
    ]

@app.get("/products/{product_id}", response_model=ProductResponse)
def list_products(product_id: int):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id= ?", (product_id,))
    product = cursor.fetchone()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    conn.close()
    return {
        "id": product[0],
        "name": product[1],
        "price": product[2],
        "stock": product[3],
    }

@app.post("/products")
def add_products(product: ProductCreate):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, stock)"
                   " VALUES (?,?,?)",
                   (product.name, product.price, product.stock))
    conn.commit()
    conn.close()
    return {
        "message": "Product added successfully",
    }

@app.get("/orders", response_model=list[OrderResponse])
def get_orders():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    conn.close()

    return [
        {
            "id": order[0],
            "product_id": order[1],
            "quantity": order[2],
            "status": order[3],
            "created_at": order[4],
        }
        for order in orders
    ]

@app.get("/orders/{order_id}", response_model=OrderResponse)
def list_orders(order_id: int):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id= ?", (order_id,))
    order = cursor.fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail="Product not found")

    conn.close()
    return {
        "id": order[0],
        "product_id": order[1],
        "quantity": order[2],
        "status": order[3],
        "created_at": order[4],
    }

@app.post("/orders", response_model=OrderResponse)
def send_orders(order: OrderCreate):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()

    # Find product

    cursor.execute("SELECT id, stock FROM products WHERE id = ?",
                   (order.product_id,))

    product = cursor.fetchone()
    if product is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    # Check stock
    if product[1] < order.quantity:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not available")

    # Create Order
    cursor.execute("INSERT INTO orders (product_id, quantity, status, created_at)"
                   " VALUES (?,?,?,?)",
                   (order.product_id, order.quantity, "open", datetime.now()))
    order_id = cursor.lastrowid

    # Reduce Stock
    cursor.execute("""
                    UPDATE products 
                    SET stock = stock - ?
                    WHERE id = ?""",
                   (order.quantity, order.product_id))

    conn.commit()

    # Get newly created order
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    created_order = cursor.fetchone()
    conn.close()

    event = {
        "event": "OrderCreated",
        "order_id": order_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
    }
    producer.send("orders", json.dumps(event).encode())
    producer.flush()

    return {
            "id": created_order[0],
            "product_id": created_order[1],
            "quantity": created_order[2],
            "status": created_order[3],
            "created_at": created_order[4],
    }

@app.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments():
    conn = sqlite3.connect("shipping/shipments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments")
    shipments = cursor.fetchall()
    conn.close()
    return [{
        "id": shipment[0],
        "order_id": shipment[1],
        "status": shipment[2],
        "created_at": shipment[3],
    }
    for shipment in shipments
    ]