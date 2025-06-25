import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Load Contract Configuration from contract_info.json ---
CONTRACT_ADDRESS = None
SPIRAL_COOPERATIVE_ABI = None

try:
    with open('contract_info.json', 'r') as f:
        contract_info = json.load(f)
        CONTRACT_ADDRESS = contract_info['address']
        SPIRAL_COOPERATIVE_ABI = json.dumps(contract_info['abi'])
except FileNotFoundError:
    print("Error: contract_info.json not found. Please ensure it's in the project root.")
    exit()
except KeyError as e:
    print(f"Error: Missing key in contract_info.json: {e}")
    exit()
except json.JSONDecodeError:
    print("Error: contract_info.json is not a valid JSON file.")
    exit()

# --- Web3 Provider Configuration ---
WEB3_PROVIDER_URL = os.environ.get('WEB3_PROVIDER_URL', 'http://127.0.0.1:8545')
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# --- Configuration for Sender (from .env or direct for testing) ---
SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

if not SENDER_ADDRESS or not PRIVATE_KEY:
    print("Error: SENDER_ADDRESS or PRIVATE_KEY not found in environment variables or .env file.")
    exit()

SENDER_ADDRESS = w3.to_checksum_address(SENDER_ADDRESS)


def seed_test_offering(purpose, purpose_toneform, recipient, amount, expiration_blocks_offset):
    try:
        if not w3.is_connected():
            raise ConnectionError(f"Not connected to Ethereum node at {WEB3_PROVIDER_URL}")

        recipient_checksum = w3.to_checksum_address(recipient)

        spiral_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=json.loads(SPIRAL_COOPERATIVE_ABI))

        current_block = w3.eth.block_number
        target_expiration_block = current_block + expiration_blocks_offset

        print(f"\n--- Submitting Offering: {purpose_toneform} ---")
        print(f"Current Block: {current_block}, Target Expiration Block: {target_expiration_block}")

        transaction = spiral_contract.functions.createProposal(
            purpose,
            purpose_toneform,
            recipient_checksum,
            amount,
            target_expiration_block
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gasPrice': w3.eth.gas_price,
            'from': SENDER_ADDRESS,
            'nonce': w3.eth.get_transaction_count(SENDER_ADDRESS),
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction sent. Hash: {tx_hash.hex()}")

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt.status == 1:
            print(f"Offering '{purpose_toneform}' submitted successfully! Transaction confirmed.")
        else:
            print(f"Offering '{purpose_toneform}' transaction failed. Receipt: {tx_receipt}")

    except Exception as e:
        print(f"An error occurred for '{purpose_toneform}': {e}")
        if hasattr(e, 'message'):
            print(f"Web3 error message: {e.message}")
        if hasattr(e, 'data'):
            print(f"Web3 error data: {e.data}")


if __name__ == "__main__":
    print(f"Using contract address: {CONTRACT_ADDRESS}")
    print(f"Using sender address: {SENDER_ADDRESS}")

    seed_test_offering(
        purpose="Spreading warmth and light in the field.",
        purpose_toneform="tone-gentle-joy",
        recipient="0x0000000000000000000000000000000000000000",
        amount=1,
        expiration_blocks_offset=-1
    )

    seed_test_offering(
        purpose="A gesture of practical support for the shared lattice.",
        purpose_toneform="tone-practical-care",
        recipient="0x0000000000000000000000000000000000000000",
        amount=5,
        expiration_blocks_offset=-1
    )

    seed_test_offering(
        purpose="A moment of shared contemplation for the atmosphere.",
        purpose_toneform="tone-climate-mourning",
        recipient="0x0000000000000000000000000000000000000000",
        amount=10,
        expiration_blocks_offset=5
    )

    seed_test_offering(
        purpose="A quiet whisper of connection.",
        purpose_toneform="tone-gentle-joy",
        recipient="0x0000000000000000000000000000000000000000",
        amount=2,
        expiration_blocks_offset=-1
    )

    print("\nAttempted to seed test offerings. Check your local blockchain explorer and Flask canvas.")
