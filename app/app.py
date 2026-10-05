import os
import threading
import time
import urllib.request
import urllib.error
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

NODE_ID = os.getenv("NODE_ID", "node-unknown")
PORT = int(os.getenv("PORT", "8080"))
PEERS = [p.strip().rstrip("/") for p in os.getenv("PEERS", "").split(",") if p.strip()]

DATA = {}
LOCK = threading.Lock()

def post_json(url, payload, timeout=1.5):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8")

def get_json(url, timeout=2):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

def replicate_to_peers(key, value):
    results = {}
    for peer in PEERS:
        try:
            post_json(f"{peer}/internal/replicate", {
                "key": key,
                "value": value,
                "source": NODE_ID
            })
            results[peer] = "OK"
        except Exception as exc:
            results[peer] = f"UNAVAILABLE: {type(exc).__name__}"
    return results

def sync_from_peer():
    while True:
        time.sleep(2)
        if not PEERS:
            continue
        for peer in PEERS:
            try:
                remote = get_json(f"{peer}/internal/data")
                remote_data = remote.get("data", {})
                if remote_data:
                    with LOCK:
                        DATA.update(remote_data)
                break
            except Exception:
                continue

@app.get("/")
def home():
    return jsonify({
        "service": "distributed-replication-tp-v2",
        "node": NODE_ID,
        "peers": PEERS
    })

@app.get("/health")
def health():
    return jsonify({
        "node": NODE_ID,
        "status": "UP",
        "data_count": len(DATA)
    })

@app.get("/data")
def get_data():
    with LOCK:
        snapshot = dict(DATA)
    return jsonify({
        "node": NODE_ID,
        "count": len(snapshot),
        "data": snapshot
    })

@app.post("/data")
def write_data():
    body = request.get_json(silent=True) or {}
    key = body.get("key")
    value = body.get("value")

    if not key or value is None:
        return jsonify({"error": "key and value are required"}), 400

    with LOCK:
        DATA[key] = value

    replication = replicate_to_peers(key, value)

    return jsonify({
        "message": "data stored and replicated",
        "node": NODE_ID,
        "item": {"key": key, "value": value},
        "replication": replication
    })

@app.post("/internal/replicate")
def internal_replicate():
    body = request.get_json(silent=True) or {}
    key = body.get("key")
    value = body.get("value")

    if not key or value is None:
        return jsonify({"error": "key and value are required"}), 400

    with LOCK:
        DATA[key] = value

    return jsonify({
        "message": "replica stored",
        "node": NODE_ID
    })

@app.get("/internal/data")
def internal_data():
    with LOCK:
        snapshot = dict(DATA)
    return jsonify({"node": NODE_ID, "data": snapshot})

@app.post("/internal/sync")
def internal_sync():
    body = request.get_json(silent=True) or {}
    incoming = body.get("data", {})
    if isinstance(incoming, dict):
        with LOCK:
            DATA.update(incoming)
    return jsonify({"message": "synchronized", "node": NODE_ID, "count": len(DATA)})

if __name__ == "__main__":
    threading.Thread(target=sync_from_peer, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
