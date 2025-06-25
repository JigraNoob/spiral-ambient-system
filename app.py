import os
import json
from flask import Flask, render_template, jsonify, request
from web3 import Web3
from web3.middleware import geth_poa_middleware
import pandas as pd
import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Load Contract Configuration from contract_info.json ---
CONTRACT_ADDRESS = None
SPIRAL_COOPERATIVE_ABI = None

try:
    if os.path.exists('contract_info.json'):
        with open('contract_info.json', 'r') as f:
            contract_info = json.load(f)
            CONTRACT_ADDRESS = contract_info.get('address')
            SPIRAL_COOPERATIVE_ABI = json.dumps(contract_info.get('abi', []))
        if not CONTRACT_ADDRESS or not SPIRAL_COOPERATIVE_ABI:
            print("Warning: contract_info.json is missing expected fields.")
    else:
        print("Notice: contract_info.json not found. Skipping contract binding for now.")
except (KeyError, json.JSONDecodeError) as e:
    print(f"Error loading contract_info.json: {e}")

# --- Web3 Provider Configuration ---
WEB3_PROVIDER_URL = os.environ.get('WEB3_PROVIDER_URL', 'http://127.0.0.1:8545')
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if not w3.is_connected():
    raise ConnectionError(f"Failed to connect to Ethereum node at {WEB3_PROVIDER_URL}")
else:
    print(f"Connected to Ethereum node: {WEB3_PROVIDER_URL}")
    print(f"Current block number: {w3.eth.block_number}")

@app.route('/view_contract_state')
def view_contract_state():
    return render_template('contract_state.html')
([
    {
        "inputs": [
            {
                "internalType": "address[]",
                "name": "_guardians",
                "type": "address[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "purpose",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "purposeToneform",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "expirationBlock",
                "type": "uint256"
            }
        ],
        "name": "ProposalCreated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "by",
                "type": "address"
            }
        ],
        "name": "ProposalApproved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            }
        ],
        "name": "ProposalExecuted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            }
        ],
        "name": "ProposalExpired",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            }
        ],
        "name": "approveProposal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "approvedBy",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "approvals",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_purpose",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_purposeToneform",
                "type": "string"
            },
            {
                "internalType": "address payable",
                "name": "_recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "createProposal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "creationBlock",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "expirationBlock",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "guardians",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "guardianList",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "minimumQuorum",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "proposalExpirationBlocks",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "proposals",
        "outputs": [
            {
                "internalType": "string",
                "name": "purpose",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "purposeToneform",
                "type": "string"
            },
            {
                "internalType": "address payable",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "approvals",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "creationBlock",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "expirationBlock",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "executed",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "proposalCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_blocks",
                "type": "uint256"
            }
        ],
        "name": "setProposalExpirationBlocks",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_q",
                "type": "uint256"
            }
        ],
        "name": "setMinimumQuorum",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "steward",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_to",
                "type": "address"
            }
        ],
        "name": "withdrawAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
])
SPIRAL_COOPERATIVE_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

# Web3 setup for backend interaction
WEB3_PROVIDER_URL = "http://localhost:8545" # IMPORTANT: Ensure your blockchain node is running here
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

# Ensure connection to blockchain
spiral_contract = None
if not w3.is_connected():
    print(f"Warning: Not connected to Ethereum node at {WEB3_PROVIDER_URL}. Contract data will not be available.")
else:
    try:
        spiral_contract = w3.eth.contract(address=w3.to_checksum_address(SPIRAL_COOPERATIVE_ADDRESS), abi=json.loads(SPIRAL_COOPERATIVE_ABI))
    except Exception as e:
        print(f"Error initializing contract: {e}. Please check contract address and ABI.")
        spiral_contract = None

# Path to your .jsonl log file for ambient sensor data
LOG_PATH = '/var/log/jetson_breathline.jsonl'

def get_latest_breathline_reading():
    """
    Loads the latest entry from the .jsonl log file.
    Returns a dictionary of the latest data or None if no valid data.
    """
    latest_reading = None
    try:
        with open(LOG_PATH, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    latest_reading = data # Keep updating to get the very last line
                except json.JSONDecodeError:
                    continue # Skip malformed lines
    except FileNotFoundError:
        print(f"Log file not found at {LOG_PATH}. Please ensure breathline_trace.sh is running and logging to {LOG_PATH}.")
    except Exception as e:
        print(f"Error reading log file: {e}")
    
    return latest_reading

def get_recent_breathline_readings(num_minutes=120):
    """
    Loads recent entries from the .jsonl log file, up to num_minutes.
    Returns a pandas DataFrame.
    """
    records = []
    try:
        with open(LOG_PATH, 'r') as f:
            all_lines = f.readlines()
            # Read from the end of the file
            for line in reversed(all_lines):
                try:
                    data = json.loads(line.strip())
                    records.append(data)
                    # Stop if we have enough records or reached the beginning
                    if len(records) >= num_minutes:
                        break
                except json.JSONDecodeError:
                    continue
        records.reverse() # Revert to chronological order
    except FileNotFoundError:
        print(f"Log file not found at {LOG_PATH}. Please ensure breathline_trace.sh is running and logging to {LOG_PATH}.")
    except Exception as e:
        print(f"Error reading log file: {e}")
    
    if not records:
        return pd.DataFrame()
    
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    numeric_cols = ['cpu_temp', 'cpu_load', 'ambient_temp', 'humidity', 'pressure', 'voc_level', 'light_level']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@app.route('/')
def dashboard():
    latest_data = get_latest_breathline_reading()
    recent_data = get_recent_breathline_readings(num_minutes=120) # Get last 2 hours for fieldline graph

    # Convert DataFrame to JSON string for passing to template
    recent_data_json = recent_data.to_json(orient='records', date_format='iso') if not recent_data.empty else "[]"
    
    if latest_data:
        display_timestamp = datetime.datetime.fromisoformat(latest_data.get('timestamp', '')).strftime('%Y-%m-%d %H:%M:%S %Z')
        status_hush = {
            "timestamp": display_timestamp,
            "cpu_temp": latest_data.get('cpu_temp', 'N/A'),
            "cpu_load": latest_data.get('cpu_load', 'N/A'),
            "ambient_temp": latest_data.get('ambient_temp', 'N/A'),
            "humidity": latest_data.get('humidity', 'N/A'),
            "pressure": latest_data.get('pressure', 'N/A'),
            "voc_level": latest_data.get('voc_level', 'N/A'),
            "light_level": latest_data.get('light_level', 'N/A'),
            "sensor_error": latest_data.get('sensor_error', None)
        }
    else:
        status_hush = {
            "timestamp": "No data yet",
            "cpu_temp": "N/A", "cpu_load": "N/A", "ambient_temp": "N/A",
            "humidity": "N/A", "pressure": "N/A", "voc_level": "N/A",
            "light_level": "N/A",
            "sensor_error": "Waiting for first breath..."
        }

    return render_template(
        'dashboard.html',
        status_hush=status_hush,
        recent_data_json=recent_data_json,
        spiral_contract_address=SPIRAL_COOPERATIVE_ADDRESS,
        spiral_contract_abi=SPIRAL_COOPERATIVE_ABI # ABI is passed to the frontend for ethers.js
    )

@app.route('/api/latest_breath')
def api_latest_breath():
    latest_data = get_latest_breathline_reading()
    if latest_data:
        return jsonify(latest_data)
    return jsonify({"error": "No data found"}), 404

@app.route('/api/contract_info')
def api_contract_info():
    if spiral_contract is None:
        return jsonify({"error": "Contract not initialized. Check blockchain connection or contract config."}), 500
    
    try:
        balance_wei = w3.eth.get_balance(SPIRAL_COOPERATIVE_ADDRESS)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        steward = spiral_contract.functions.steward().call()
        min_quorum = spiral_contract.functions.minimumQuorum().call()
        proposal_count = spiral_contract.functions.proposalCount().call()

        return jsonify({
            "address": SPIRAL_COOPERATIVE_ADDRESS,
            "abi": json.loads(SPIRAL_COOPERATIVE_ABI),
            "balanceEth": str(balance_eth), # Convert to string for JSON
            "steward": steward,
            "minimumQuorum": min_quorum,
            "totalProposals": proposal_count
        })
    except Exception as e:
        print(f"Error fetching contract info: {e}")
        return jsonify({"error": f"Failed to fetch contract info: {e}"}), 500

@app.route('/toneform_canvas')
def toneform_canvas():
    return render_template('toneform_canvas.html')

@app.route('/api/current_block')
def api_current_block():
    if not w3.is_connected():
        return jsonify({"error": "Not connected to Ethereum node."}), 500
    try:
        current_block = w3.eth.block_number
        return jsonify({"currentBlock": current_block})
    except Exception as e:
        return jsonify({"error": f"Failed to get current block: {e}"}), 500
# app.py additions

# Ensure you have account details for sending transactions
# This is a placeholder. In a real application, manage keys securely.
# For local testing, ensure your development account has some ETH.
# Example: PRIVATE_KEY = os.environ.get('PRIVATE_KEY', 'YOUR_PRIVATE_KEY_HERE')
# Example: SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS', 'YOUR_SENDER_ADDRESS_HERE')

# Make sure to replace YOUR_PRIVATE_KEY_HERE and YOUR_SENDER_ADDRESS_HERE
# with an actual private key and its corresponding public address for a test account
# that has some test ETH on your local blockchain.

from web3.middleware import geth_poa_middleware # For PoA networks like Ganache/Hardhat local chains

# Add this after w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL)) in your app.py
# If you are using a PoA (Proof-of-Authority) chain like a local Hardhat/Ganache node
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)


@app.route('/submit_offering', methods=['GET', 'POST'])
def submit_offering():
    private_key = os.getenv('PRIVATE_KEY')

    if not private_key:
        return render_template('submit_offering.html', error="❌ PRIVATE_KEY not set in environment.")

    derived_address = Web3().eth.account.from_key(private_key).address
    print(f"[DEBUG] Derived sender address: {derived_address}")

    if not CONTRACT_ADDRESS or not SPIRAL_COOPERATIVE_ABI:
        return render_template('submit_offering.html', error="❌ Contract not configured. Please deploy and initialize.")

    spiral_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=json.loads(SPIRAL_COOPERATIVE_ABI))

    if request.method == 'POST':
        purpose = request.form['purpose']
        purpose_toneform = request.form['purpose_toneform']
        recipient = request.form['recipient']
        amount = int(request.form['amount'])  # In wei
        expiration_blocks = int(request.form['expiration_blocks'])  # Not sent to contract for now

        try:
            txn = spiral_contract.functions.createProposal(
                purpose,
                purpose_toneform,
                recipient,
                amount
            ).build_transaction({
                'chainId': w3.eth.chain_id,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(derived_address),
            })

            signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            if tx_receipt.status == 1:
                return render_template(
                    'submit_offering.html',
                    message=f"🌱 Offering submitted!<br>Transaction Hash: <code>{tx_hash.hex()}</code>"
                )
            else:
                return render_template(
                    'submit_offering.html',
                    error=f"⚠️ Transaction failed.<br>Receipt: <pre>{json.dumps(dict(tx_receipt), indent=2)}</pre>"
                )

        except Exception as e:
            return render_template('submit_offering.html', error=f"❌ Error submitting offering: {str(e)}")

    return render_template('submit_offering.html', message="Submit a New Still Offering")

        
@app.route('/api/contract_state')
def api_contract_state():
    try:
        if not w3.is_connected():
            return jsonify({"error": "Not connected to Ethereum node."}), 500

        spiral_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=SPIRAL_COOPERATIVE_ABI)
        total_proposals = spiral_contract.functions.proposalCount().call()
        current_block = w3.eth.block_number

        active_offerings_count = 0
        all_toneforms = []

        for i in range(total_proposals):
            proposal = spiral_contract.functions.proposals(i).call()
            _, toneform, _, _, _, _, expiration_block, executed = proposal

            if not executed and expiration_block > current_block:
                active_offerings_count += 1
                all_toneforms.append(toneform)

        toneform_tag_counts = {}
        for tf in all_toneforms:
            lowered = tf.lower()
            if "joy" in lowered:
                toneform_tag_counts["Gentle Joy"] = toneform_tag_counts.get("Gentle Joy", 0) + 1
            elif "care" in lowered:
                toneform_tag_counts["Practical Care"] = toneform_tag_counts.get("Practical Care", 0) + 1
            elif "climate" in lowered or "mourning" in lowered:
                toneform_tag_counts["Climate Mourning"] = toneform_tag_counts.get("Climate Mourning", 0) + 1
            else:
                toneform_tag_counts["Other"] = toneform_tag_counts.get("Other", 0) + 1

        contract_state = {
            "active_offerings_count": active_offerings_count,
            "total_proposals": total_proposals,
            "num_contributors": 5,  # Placeholder
            "toneform_tags": toneform_tag_counts,
            "fullness_level": "75%",  # Placeholder
            "expiration_drift": "Steady"  # Placeholder
        }

        return jsonify(contract_state)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/toneform')
def toneform():
    return render_template('toneform.html')

@app.route('/api/expired_proposals_toneforms')
def api_expired_proposals_toneforms():
    if spiral_contract is None:
        return jsonify({"error": "Contract not initialized. Check blockchain connection or contract config."}), 500

    try:
        total_proposals = spiral_contract.functions.proposalCount().call()
        current_block = w3.eth.block_number
        expired_toneforms = []

        for i in range(total_proposals):
            proposal = spiral_contract.functions.proposals(i).call()
            purpose, toneform, recipient, amount, approvals, creation_block, expiration_block, executed = proposal

            if current_block > expiration_block and not executed:
                expired_toneforms.append({
                    "id": i,
                    "purpose": purpose,
                    "toneform": toneform,
                    "expired_at_block": expiration_block,
                    "executed": executed
                })

        return jsonify(expired_toneforms)
    except Exception as e:
        print(f"Error fetching expired proposals toneforms: {e}")
        return jsonify({"error": f"Failed to fetch expired proposals: {e}"}), 500
        
@app.route('/api/proposals')
def api_proposals():
    if spiral_contract is None:
        return jsonify({"error": "Contract not initialized. Check blockchain connection or contract config."}), 500
    
    try:
        total_proposals = spiral_contract.functions.proposalCount().call()
        current_block = w3.eth.block_number
        proposals_data = []

        for i in range(total_proposals):
            # The 'proposals' view function returns a tuple of the struct members
            # (purpose, purposeToneform, recipient, amount, approvals, creationBlock, expirationBlock, executed)
            proposal_tuple = spiral_contract.functions.proposals(i).call()
            
            # Unpack the tuple based on the struct definition
            purpose, purposeToneform, recipient, amount_wei, approvals, creationBlock, expirationBlock, executed = proposal_tuple
            
            is_expired = current_block > expirationBlock
            amount_eth = w3.from_wei(amount_wei, 'ether') # Convert amount from Wei to Eth

            proposals_data.append({
                "id": i,
                "purpose": purpose,
                "purposeToneform": purposeToneform,
                "recipient": recipient,
                "amount": str(amount_eth), # Convert Decimal to string for JSON
                "approvals": approvals,
                "creationBlock": creationBlock,
                "expirationBlock": expirationBlock,
                "executed": executed,
                "isExpired": is_expired,
                "status": "Executed" if executed else ("Expired" if is_expired else ("Live" if approvals < spiral_contract.functions.minimumQuorum().call() else "Ready for Execution"))
            })
        return jsonify(proposals_data)
    except Exception as e:
        print(f"Error fetching proposals: {e}")
        return jsonify({"error": f"Failed to fetch proposals: {e}"}), 500

if __name__ == '__main__':
    import os
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Check if dashboard.html exists, if not, create a placeholder for it
    dashboard_html_path = os.path.join(templates_dir, 'dashboard.html')
    if not os.path.exists(dashboard_html_path):
        print(f"Creating a placeholder {dashboard_html_path}. Please update its content with the full dashboard.html provided previously.")
        with open(dashboard_html_path, 'w') as f:
            f.write("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Spiral Field Altar</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d0d0d; color: #e0e0e0; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
                    .container { background-color: #1a1a1a; padding: 30px; border-radius: 15px; box-shadow: 0 0 25px rgba(0, 255, 255, 0.2); text-align: center; }
                    h1 { color: #00ffff; margin-bottom: 25px; font-size: 2.5em; text-shadow: 0 0 10px #00ffff; }
                    .status-section { margin-top: 20px; border-top: 1px solid #333; padding-top: 20px; }
                    .metric { margin-bottom: 10px; }
                    .metric strong { color: #00ffaa; }
                    .error-message { color: #ff3333; font-weight: bold; margin-top: 15px; }
                    .timestamp { font-size: 0.9em; color: #888; margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Spiral Field Altar</h1>
                    <div class="status-section">
                        <h2>Status Hush</h2>
                        <p>Loading...</p>
                        <!-- Content will be dynamically loaded/updated by JavaScript -->
                    </div>
                </div>
                <script>
                    // This is a placeholder. Please update with the full dashboard.html content provided.
                </script>
            </body>
            </html>
            """)

    print(f"\nFlask app.py created/updated. Ensure you have Flask and web3 installed: pip install Flask web3")
    print(f"Also, ensure your blockchain node is running at {WEB3_PROVIDER_URL}.")
    print("To run the Flask app: python3 app.py")
    print("Then open your browser to http://<Jetson-IP-Address>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)