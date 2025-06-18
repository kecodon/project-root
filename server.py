# server.py
import os
import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

# Database path
DB_PATH = 'database/hiveos.db'

# Ensure DB folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Init DB if not exists
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS wallets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        coin TEXT,
                        source TEXT,
                        address TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS flight_sheets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        coin TEXT,
                        wallet TEXT,
                        pool TEXT,
                        miner TEXT
                    )''')
        conn.commit()

init_db()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Wallet(BaseModel):
    coin: str
    source: str
    address: str

class FlightSheet(BaseModel):
    name: str
    coin: str
    wallet: str
    pool: str
    miner: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/wallets", response_class=HTMLResponse)
async def wallets_page(request: Request):
    return templates.TemplateResponse("wallets.html", {"request": request})

@app.get("/flight_sheets", response_class=HTMLResponse)
async def flight_sheets_page(request: Request):
    wallets = []
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        wallets = c.execute("SELECT * FROM wallets").fetchall()
    return templates.TemplateResponse("flight_sheets.html", {"request": request, "wallets": wallets})

# API for Wallets
@app.get("/api/wallets")
async def get_wallets():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        wallets = conn.execute("SELECT * FROM wallets").fetchall()
        return JSONResponse([dict(w) for w in wallets])

@app.post("/api/wallets")
async def add_wallet(wallet: Wallet):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO wallets (coin, source, address) VALUES (?, ?, ?)",
                     (wallet.coin, wallet.source, wallet.address))
        conn.commit()
    return {"status": "ok"}

# API for Flight Sheets
@app.get("/api/flight_sheets")
async def get_flight_sheets():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        sheets = conn.execute("SELECT * FROM flight_sheets").fetchall()
        return JSONResponse([dict(s) for s in sheets])

@app.post("/api/flight_sheets")
async def add_flight_sheet(sheet: FlightSheet):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO flight_sheets (name, coin, wallet, pool, miner) VALUES (?, ?, ?, ?, ?)",
                     (sheet.name, sheet.coin, sheet.wallet, sheet.pool, sheet.miner))
        conn.commit()
    return {"status": "ok"}

@app.post("/api/flight_sheets/delete")
async def delete_flight_sheet(name: str = Form(...)):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM flight_sheets WHERE name=?", (name,))
        conn.commit()
    return {"status": "deleted"}
@app.post("/api/wallets/add")
async def add_wallet(wallet: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wallets (name, address, coin) VALUES (?, ?, ?)
    ''', (wallet["name"], wallet["address"], wallet["coin"]))
    conn.commit()
    conn.close()
    return {"message": "Wallet added successfully"}
@app.get("/api/flight-sheets/list")
async def list_flight_sheets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, coin, wallet, pool, miner FROM flight_sheets")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "coin": row[1], "wallet": row[2], "pool": row[3], "miner": row[4]} for row in rows]


@app.post("/api/flight-sheets/add")
async def add_flight_sheet(sheet: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flight_sheets (coin, wallet, pool, miner) VALUES (?, ?, ?, ?)
    ''', (sheet["coin"], sheet["wallet"], sheet["pool"], sheet["miner"]))
    conn.commit()
    conn.close()
    return {"message": "Flight Sheet added"}
