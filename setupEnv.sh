#!/bin/bash

if [ ! -f ".venv/bin/activate" ]; then
    pip3 install virtualenv
    python3 -m venv .venv
fi

if [ ! -f ".venv/bin/activate" ]; then
    exit 1
fi

source .venv/bin/activate

