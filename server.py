from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel
from typing import List
import json
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

wallet_file = DATA_DIR / "wallets.json"
flight_sheet_file = DATA_DIR / "flight_sheets.json"

class Wallet(BaseModel):
    coin: str
    source: str
    address: str

class FlightSheet(BaseModel):
    coin: str
    wallet: str
    pool: str
    miner: str
    name: str

def load_json_file(file):
    if file.exists():
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_json_file(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse("""
        <html><head><meta http-equiv="refresh" content="0; url=/flight_sheets"/></head><body></body></html>
    """)

@app.get("/wallets", response_class=HTMLResponse)
async def wallets_page(request: Request):
    return templates.TemplateResponse("wallets.html", {"request": request})

@app.get("/flight_sheets", response_class=HTMLResponse)
async def flight_sheets_page(request: Request):
    wallets = load_json_file(wallet_file)
    flightsheets = load_json_file(flight_sheet_file)
    return templates.TemplateResponse("flight_sheets.html", {
        "request": request,
        "wallets": wallets,
        "flightsheets": flightsheets
    })

@app.get("/api/wallets")
async def get_wallets():
    return load_json_file(wallet_file)

@app.post("/api/wallets")
async def add_wallet(wallet: Wallet):
    wallets = load_json_file(wallet_file)
    wallets.append(wallet.dict())
    save_json_file(wallet_file, wallets)
    return {"status": "ok"}

@app.post("/api/flight_sheet")
async def create_flight_sheet(sheet: FlightSheet):
    sheets = load_json_file(flight_sheet_file)
    sheets.append(sheet.dict())
    save_json_file(flight_sheet_file, sheets)
    return {"status": "ok"}

@app.post("/api/flight_sheet/delete")
async def delete_flight_sheet(request: Request):
    body = await request.json()
    name = body.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Missing name")
    sheets = load_json_file(flight_sheet_file)
    sheets = [s for s in sheets if s["name"] != name]
    save_json_file(flight_sheet_file, sheets)
    return {"status": "deleted"}
