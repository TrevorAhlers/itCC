import sqlite3
from datetime import datetime

DB_NAME = "history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            price TEXT,
            change TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_search(ticker, price, change):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO searches (ticker, price, change, timestamp)
        VALUES (?, ?, ?, ?)
    """, (ticker, price, change, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT ticker, price, change, timestamp FROM searches ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows