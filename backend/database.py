import sqlite3
conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS products (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL UNIQUE,
               price INTEGER NOT NULL,
               stock INTEGER NOT NULL
               )
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               product_id INTEGER NOT NULL, 
               quantity INTEGER NOT NULL, 
               status TEXT NOT NULL, 
               created_at TIMESTAMP NOT NULL,
               FOREIGN KEY (product_id) REFERENCES products(id)
               )
               """)