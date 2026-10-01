import sqlite3
conn = sqlite3.connect('shipping/shipments.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS shipments (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               order_id INTEGER NOT NULL,
               status TEXT NOT NULL,
               created_at TIMESTAMP NOT NULL         
               )
               """)