#!/bin/bash

echo "==============================================="
echo "  Dacarsoft Finance Bot - Starting..."
echo "==============================================="
echo ""

# Activate virtual environment
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create a .env file with your configuration."
    echo "See example_env.txt for reference."
    exit 1
fi

# Start the bot
python main.py

