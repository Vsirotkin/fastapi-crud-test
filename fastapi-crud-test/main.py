import os
import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Инициализация FastAPI
app = FastAPI(title="FastAPI CRUD Test for AI IDE BAS")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Item(ItemCreate):
    id: int

# Работа с SQLite
DB_FILE = "test.db"

def init_db():
    print(f"[DB] FULL PATH: {os.path.abspath(DB_FILE)}")  # 👈 вот это важно
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Контекстный менеджер для подключения к БД
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Инициализация БД при старте
init_db()

# === Эндпоинты ===

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    print(f"Received item: name={item.name}, description={item.description}")  # 👈
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (item.name, item.description)
        )
        conn.commit()
        item_id = cursor.lastrowid
        print(f"Inserted item with ID: {item_id}")  # 👈
        return {"id": item_id, "name": item.name, "description": item.description}

@app.get("/items", response_model=List[Item])
def read_items():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM items")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(row)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET name = ?, description = ? WHERE id = ?",
            (item.name, item.description, item_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": item_id, "name": item.name, "description": item.description}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted"}


if __name__ == "__main__":
    main()
