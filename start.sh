#!/bin/bash

echo "🌱 Breathing life into Spiral Field Altar..."

# Activate virtual environment
VENV_PATH="./venv310"
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "🌀 Virtual environment activated."
else
    echo "⚠️  Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Load environment variables safely
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
    echo "🔐 Environment variables loaded."
else
    echo "⚠️  .env file not found."
    exit 1
fi

# Start Hardhat if not running
if ! nc -z localhost 8545; then
    echo "🔧 Starting Hardhat node..."
    npx hardhat node > hardhat.log 2>&1 &
    HARDHAT_PID=$!
    sleep 6
    echo "⛓️  Hardhat node launched (PID: $HARDHAT_PID)"
else
    echo "⛓️  Hardhat node already running."
fi

# Start Flask
echo "🕯️  Launching Flask altar..."
python3 app.py
