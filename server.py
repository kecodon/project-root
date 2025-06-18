from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

workers = {}
wallets = []
flight_sheets = []

@app.route("/")
def index():
    return render_template("index.html", workers=workers)

@app.route("/wallets")
def wallet_page():
    return render_template("wallets.html", wallets=wallets)

@app.route("/flight_sheets")
def flight_sheets_page():
    return render_template("flight_sheets.html", flight_sheets=flight_sheets, wallets=wallets)

@app.route("/api/config")
def get_config():
    worker = request.args.get("worker")
    for fs in flight_sheets:
        if fs.get("applied") and worker in fs.get("applied_workers", []):
            return jsonify(fs)
    return jsonify({})

@app.route("/api/report", methods=["POST"])
def report_status():
    data = request.json
    worker = data.get("worker")
    data["last_seen"] = datetime.now().isoformat()
    workers[worker] = data
    return jsonify({"ok": True})

@app.route("/api/wallet", methods=["POST"])
def add_wallet():
    data = request.json
    wallets.append(data)
    return jsonify({"ok": True})

@app.route("/api/flight_sheet", methods=["POST"])
def add_flight_sheet():
    data = request.json
    fs_name = data.get("name")
    exists = next((f for f in flight_sheets if f["name"] == fs_name), None)
    if exists:
        flight_sheets.remove(exists)
    data["applied_workers"] = []
    data["applied"] = False
    flight_sheets.append(data)
    return jsonify({"ok": True})

@app.route("/api/apply_all", methods=["POST"])
def apply_all():
    fs_name = request.json.get("flight_sheet")
    for fs in flight_sheets:
        fs["applied"] = (fs["name"] == fs_name)
        if fs["applied"]:
            fs["applied_workers"] = list(workers.keys())
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
@app.route('/api/flight_sheets', methods=['POST'])
def save_flight_sheet():
    data = request.json

    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    flight_sheets = []
    if os.path.exists('flight_sheets.json'):
        with open('flight_sheets.json') as f:
            flight_sheets = json.load(f)

    flight_sheets.append(data)

    with open('flight_sheets.json', 'w') as f:
        json.dump(flight_sheets, f, indent=2)

    return jsonify({'status': 'success'})
@app.route('/flight_sheets')
def flight_sheets():
    # Load wallets
    wallets = []
    if os.path.exists('wallets.json'):
        with open('wallets.json') as f:
            wallets = json.load(f)

    # Load flight sheets
    flight_sheets = []
    if os.path.exists('flight_sheets.json'):
        with open('flight_sheets.json') as f:
            flight_sheets = json.load(f)

    return render_template('flight_sheets.html', wallets=wallets, flight_sheets=flight_sheets)
