### cpu-agent/agent.py
import requests
import subprocess
import time
import json
from config import SERVER_URL, WORKER_NAME, XMRIG_PATH

while True:
    try:
        print(f"Fetching config from {SERVER_URL}/api/config?worker={WORKER_NAME}")
        res = requests.get(f"{SERVER_URL}/api/config", params={"worker": WORKER_NAME})
        config = res.json()

        print(f"Fetched config from server: {config}")

        if not config.get("miner"):
            print("No config received. Sleeping...")
            time.sleep(15)
            continue

        args = [XMRIG_PATH, "-o", config["pool"], "-u", config["wallet"]] + config.get("args", "").split()
        print("Running:", " ".join(args))

        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            line = proc.stdout.readline()
            if not line:
                break
            decoded = line.decode(errors='ignore')
            print(decoded.strip())

            if "speed" in decoded:
                try:
                    hashrate = decoded.split("speed:")[1].split()[0]
                    requests.post(f"{SERVER_URL}/api/report", json={"worker": WORKER_NAME, "status": "online", "hashrate": hashrate})
                except:
                    pass

        proc.wait()
    except Exception as e:
        print("Error:", e)
        time.sleep(15)

