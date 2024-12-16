#!/bin/bash

# Function to deactivate virtualenv and exit
cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Deactivating virtual environment"
        deactivate
    fi
    exit 0
}

# Trap SIGINT (Ctrl + C) and call cleanup
trap cleanup SIGINT

# Start the weather service

# Check if running inside Docker
if [ -f /.dockerenv ]; then
    echo "Running inside Docker"
    python3 weather.py
else
    echo "Running on local machine"
    source .venv/bin/activate
    python3 server.py
    deactivate
fi
