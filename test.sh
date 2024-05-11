#!/bin/bash

# Activate the virtual environment
source ./.venv/bin/activate

cd "$(dirname "$0")/src/tests"

python3 -m unittest discover

# Deactivate the virtual environment
deactivate