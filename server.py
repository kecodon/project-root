### server.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

workers = {
    'rig01': {
        'status': 'online',
        'hashrate': '0 H/s',
        'last_seen': datetime.datetime.now(),
        'config': {
            'tool': 'xmrig',
            'wallet': 'NHbSHmqm1ojuTRtdwkURwhamQ1pNC9SkJU9T',
            'pool': 'randomxmonero.auto.nicehash.com:9200',
            'extra_args': '-a rx/0'
        }
    }
}
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
