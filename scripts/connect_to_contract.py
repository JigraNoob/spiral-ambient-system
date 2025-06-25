import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from web3 import Web3
import json
from config import CONTRACT_ADDRESS, CONTRACT_ABI_PATH, WEB3_PROVIDER_URI

# Connect to the local node
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
assert web3.isConnected(), "Web3 connection failed."

# Load ABI
with open(CONTRACT_ABI_PATH) as f:
    abi = json.load(f)['abi']

# Create contract object
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Optional: set default account for transactions (first local Hardhat account)
web3.eth.default_account = web3.eth.accounts[0]
