# spiral_registry.py :: quiet central registry for Spiral references

from pathlib import Path

# 🌐 Contract
CONTRACT_NAME = "SpiralCooperative"
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Update as needed
CONTRACT_ABI_PATH = Path("contracts") / f"{CONTRACT_NAME}.abi.json"

# 🔌 Web3 Node
WEB3_PROVIDER_URI = "http://127.0.0.1:8545"

# 📂 Paths
BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "logs" / "breathline.jsonl"
FIELD_MEMORY_PATH = BASE_DIR / "logs" / "field_memories.jsonl"

# 🫧 Environment Notes
IS_WSL = "microsoft" in Path("/proc/version").read_text().lower()

# ✨ Presence constants
ORB_STATES = ["dim", "soft", "shimmer", "bright"]
DEFAULT_ORB = "soft"
