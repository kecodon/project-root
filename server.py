# === Cấu trúc thư mục ===
# project-root/
# ├── server.py
# ├── templates/
# │   ├── index.html
# │   ├── wallets.html
# │   ├── flight_sheets.html
# │   └── navbar.html
# ├── static/
# │   └── js/
# │       ├── wallets.js
# │       └── flight_sheets.js
# └── database/
#     └── hiveos.db

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import sqlite3
import os

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "hiveos.db")

# Đăng ký static và templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# === INIT DB ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        coin TEXT,
        address TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS flight_sheets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        coin TEXT,
        wallet_id INTEGER,
        pool TEXT,
        miner TEXT,
        FOREIGN KEY(wallet_id) REFERENCES wallets(id)
    )''')
    conn.commit()
    conn.close()

init_db()

# === MODELS ===
class Wallet(BaseModel):
    name: str
    coin: str
    address: str

class FlightSheet(BaseModel):
    name: str
    coin: str
    wallet_id: int
    pool: str
    miner: str

# === ROUTES ===
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/wallets", response_class=HTMLResponse)
def wallets_page(request: Request):
    return templates.TemplateResponse("wallets.html", {"request": request})

@app.get("/flight_sheets", response_class=HTMLResponse)
def flight_sheets_page(request: Request):
    return templates.TemplateResponse("flight_sheets.html", {"request": request})

# === API: Wallets ===
@app.get("/api/wallets")
def get_wallets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, coin, address FROM wallets")
    data = [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]
    conn.close()
    return data

@app.post("/api/wallets")
def add_wallet(wallet: Wallet):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO wallets (name, coin, address) VALUES (?, ?, ?)", (wallet.name, wallet.coin, wallet.address))
    conn.commit()
    conn.close()
    return {"status": "ok"}

# === API: Flight Sheets ===
@app.get("/api/flight_sheets")
def get_flight_sheets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT fs.id, fs.name, fs.coin, fs.pool, fs.miner, w.name as wallet_name
        FROM flight_sheets fs
        JOIN wallets w ON fs.wallet_id = w.id
    """)
    data = [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]
    conn.close()
    return data

@app.post("/api/flight_sheets")
def add_flight_sheet(sheet: FlightSheet):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO flight_sheets (name, coin, wallet_id, pool, miner) VALUES (?, ?, ?, ?, ?)",
              (sheet.name, sheet.coin, sheet.wallet_id, sheet.pool, sheet.miner))
    conn.commit()
    conn.close()
    return {"status": "ok"}
