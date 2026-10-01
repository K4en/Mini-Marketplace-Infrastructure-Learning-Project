from kafka import KafkaConsumer
import json
import urllib.request
import sqlite3
from datetime import datetime

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers=["kafka:9093"],
    auto_offset_reset="earliest",
    group_id="order-processor",
)

print("Listening...")

for message in consumer:
    event = json.loads(message.value.decode())
    print("Received:", event)
    order_id = event["order_id"]

    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'processed' WHERE id = ?",
                   (order_id,))
    conn.commit()
    conn.close()


    conn = sqlite3.connect("shipping/shipments.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shipments (order_id, status, created_at)"
                   " VALUES (?, ?, ?)",
                   (order_id, "processing", datetime.now()))
    conn.commit()
    conn.close()

