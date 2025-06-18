
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    wallets = json.load(open("data/wallets.json")) if os.path.exists("data/wallets.json") else []
    flightsheets = json.load(open("data/flight_sheets.json")) if os.path.exists("data/flight_sheets.json") else []
    return templates.TemplateResponse("flight_sheets.html", {"request": request, "wallets": wallets, "flightsheets": flightsheets})

@app.get("/wallets", response_class=HTMLResponse)
def wallets_page(request: Request):
    wallets = json.load(open("data/wallets.json")) if os.path.exists("data/wallets.json") else []
    return templates.TemplateResponse("wallets.html", {"request": request, "wallets": wallets})

@app.get("/api/status")
def status():
    return {"status": "server running on port 6001"}
