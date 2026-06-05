from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Connect to your database
DB = psycopg2.connect(
    host="localhost",
    database="ecommerce_database",
    user="postgres",
    password="Bhushan@#$12"   # ← change this to your pgAdmin password
)

class OrderCreate(BaseModel):
    user_id: int
    items: list[dict]

@app.get("/users")
def get_users():
    cur = DB.cursor()
    cur.execute("SELECT user_id, name, email FROM users")
    rows = cur.fetchall()
    return [{"user_id": r[0], "name": r[1], "email": r[2]} for r in rows]

@app.get("/products")
def get_products():
    cur = DB.cursor()
    cur.execute("SELECT product_id, title, price, stock_quantity FROM products")
    rows = cur.fetchall()
    return [{"product_id": r[0], "title": r[1], "price": float(r[2]), "stock": r[3]} for r in rows]

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    cur = DB.cursor()
    cur.execute("""
        SELECT o.order_id, u.name, o.status,
               json_agg(json_build_object(
                 'product', p.title,
                 'qty', oi.quantity,
                 'unit_price', oi.unit_price
               )) AS items
        FROM orders o
        JOIN users u ON u.user_id = o.user_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE o.order_id = %s
        GROUP BY o.order_id, u.name, o.status
    """, (order_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": row[0], "customer": row[1], "status": row[2], "items": row[3]}

@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    cur = DB.cursor()
    cur.execute(
        "INSERT INTO orders (user_id) VALUES (%s) RETURNING order_id",
        (order.user_id,)
    )
    order_id = cur.fetchone()[0]
    for item in order.items:
        cur.execute("SELECT price FROM products WHERE product_id = %s", (item["product_id"],))
        price = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s,%s,%s,%s)",
            (order_id, item["product_id"], item["quantity"], price)
        )
        cur.execute(
            "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
            (item["quantity"], item["product_id"])
        )
    DB.commit()
    return {"order_id": order_id}