from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WALLETS_FILE = "wallets.json"
FLIGHT_SHEETS_FILE = "flight_sheets.json"

# Ensure storage files exist
for file in [WALLETS_FILE, FLIGHT_SHEETS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

class Wallet(BaseModel):
    coin: str
    name: str
    address: str

class MinerConfig(BaseModel):
    miner: str
    options: dict

class FlightSheet(BaseModel):
    coin: str
    wallet: str
    pool: str
    miner_config: MinerConfig
    name: str

# Wallets endpoints
@app.get("/api/wallets", response_model=List[Wallet])
def get_wallets():
    with open(WALLETS_FILE, 'r') as f:
        return json.load(f)

@app.post("/api/wallets")
def add_wallet(wallet: Wallet):
    with open(WALLETS_FILE, 'r') as f:
        wallets = json.load(f)
    wallets.append(wallet.dict())
    with open(WALLETS_FILE, 'w') as f:
        json.dump(wallets, f, indent=2)
    return {"status": "ok"}

# Flight sheets endpoints
@app.get("/api/flight_sheets", response_model=List[FlightSheet])
def get_flight_sheets():
    with open(FLIGHT_SHEETS_FILE, 'r') as f:
        return json.load(f)

@app.post("/api/flight_sheets")
def add_flight_sheet(flight_sheet: FlightSheet):
    with open(FLIGHT_SHEETS_FILE, 'r') as f:
        flight_sheets = json.load(f)
    flight_sheets.append(flight_sheet.dict())
    with open(FLIGHT_SHEETS_FILE, 'w') as f:
        json.dump(flight_sheets, f, indent=2)
    return {"status": "ok"}

# Test route
@app.get("/")
def read_root():
    return {"status": "server running on port 6001"}
