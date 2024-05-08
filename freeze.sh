#!/bin/bash

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment does not exist. Please run setup.sh first."
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "requirements.txt already exists. Installing.."
    export FORCE_CMAKE=1
    export CMAKE_ARGS=-DLLAMA_CUBLAS=on
    pip3 install -r requirements.txt  --force-reinstall --upgrade --no-cache-dir
    echo "requirements.txt installed successfully."
else
    echo "requirements.txt does not exist. Creating one with .venv libraries..."
    pip3 freeze > requirements.txt
    echo "requirements.txt created successfully."
fi