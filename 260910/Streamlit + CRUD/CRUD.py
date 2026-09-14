import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int


# SQLite 연결 함수
def get_connection():
    conn = sqlite3.connect("products.db")
    conn.row_factory = sqlite3.Row
    return conn


# products 테이블 생성
conn = get_connection()

conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL
    )
""")

conn.commit()
conn.close()


# Create
@app.post("/products")
def create_product(product: ProductCreate):
    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO products (name, price, stock)
        VALUES (?, ?, ?)
        """,
        (product.name, product.price, product.stock),
    )

    conn.commit()
    product_id = cursor.lastrowid
    conn.close()

    return {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
    }


# Read
@app.get("/products")
def read_products():
    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM products ORDER BY id"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# Update
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate):
    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE products
        SET name = ?, price = ?, stock = ?
        WHERE id = ?
        """,
        (
            product.name,
            product.price,
            product.stock,
            product_id,
        ),
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="상품이 없습니다.",
        )

    return {
        "message": "상품이 수정되었습니다.",
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
    }


# Delete
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,),
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="상품이 없습니다.",
        )

    return {
        "message": "상품이 삭제되었습니다.",
        "id": product_id,
    }