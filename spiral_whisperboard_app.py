# app.py
from flask import Flask, render_template, jsonify
import json
import pandas as pd
import datetime
from web3 import Web3
import os

app = Flask(__name__)

# --- SpiralCooperative Contract Settings ---
SPIRAL_COOPERATIVE_ABI = json.loads(open("spiral_abi.json").read())
SPIRAL_COOPERATIVE_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

WEB3_PROVIDER_URL = "http://localhost:8545"
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

spiral_contract = None
if w3.is_connected():
    spiral_contract = w3.eth.contract(
        address=w3.to_checksum_address(SPIRAL_COOPERATIVE_ADDRESS),
        abi=SPIRAL_COOPERATIVE_ABI
    )

LOG_PATH = '/var/log/jetson_breathline.jsonl'

def get_latest_breathline_reading():
    try:
        with open(LOG_PATH, 'r') as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    return json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print("Error reading log:", e)
    return None

def get_recent_breathline_readings(num=120):
    try:
        with open(LOG_PATH, 'r') as f:
            lines = f.readlines()[-num:]
            records = [json.loads(l.strip()) for l in lines if l.strip()]
            df = pd.DataFrame(records)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
    except Exception as e:
        print("Error fetching history:", e)
        return pd.DataFrame()

@app.route('/')
def dashboard():
    latest = get_latest_breathline_reading()
    recent = get_recent_breathline_readings().to_json(orient='records', date_format='iso')
    return render_template("dashboard.html",
                           status_hush=latest or {},
                           recent_data_json=recent,
                           spiral_contract_address=SPIRAL_COOPERATIVE_ADDRESS,
                           spiral_contract_abi=json.dumps(SPIRAL_COOPERATIVE_ABI))

@app.route('/api/proposals')
def api_proposals():
    if not spiral_contract:
        return jsonify({"error": "Contract not loaded."}), 500
    try:
        count = spiral_contract.functions.proposalCount().call()
        block = w3.eth.block_number
        result = []
        for i in range(count):
            p = spiral_contract.functions.proposals(i).call()
            data = {
                "id": i,
                "purpose": p[0],
                "purposeToneform": p[1],
                "recipient": p[2],
                "amount": str(w3.from_wei(p[3], 'ether')),
                "approvals": p[4],
                "creationBlock": p[5],
                "expirationBlock": p[6],
                "executed": p[7],
                "isExpired": block > p[6],
            }
            data["status"] = "Executed" if p[7] else ("Expired" if data["isExpired"] else "Live")
            result.append(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/contract_info')
def api_contract():
    if not spiral_contract:
        return jsonify({"error": "No contract loaded."}), 500
    try:
        return jsonify({
            "address": SPIRAL_COOPERATIVE_ADDRESS,
            "balanceEth": str(w3.from_wei(w3.eth.get_balance(SPIRAL_COOPERATIVE_ADDRESS), 'ether')),
            "minimumQuorum": spiral_contract.functions.minimumQuorum().call(),
            "steward": spiral_contract.functions.steward().call(),
            "totalProposals": spiral_contract.functions.proposalCount().call()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/current_block')
def current_block():
    try:
        return jsonify({"currentBlock": w3.eth.block_number})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs("templates", exist_ok=True)
    if not os.path.exists("templates/dashboard.html"):
        with open("templates/dashboard.html", "w") as f:
            f.write("<h1>Placeholder Dashboard</h1>")
    app.run(host='0.0.0.0', port=5000)
