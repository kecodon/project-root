# init_db.py
import sqlite3
import os

DB_PATH = "database/hiveos.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Bảng wallets
cursor.execute('''
CREATE TABLE IF NOT EXISTS wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    coin TEXT
)
''')

# Bảng flight_sheets
cursor.execute('''
CREATE TABLE IF NOT EXISTS flight_sheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin TEXT,
    wallet TEXT,
    pool TEXT,
    miner TEXT
)
''')

conn.commit()
conn.close()
print(f"✅ SQLite database initialized at {DB_PATH}")
