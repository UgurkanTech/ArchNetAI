@echo off
If Not Exist ".venv\Scripts\activate.bat" (
    pip install virtualenv
    python -m venv .venv
)

If Not Exist ".venv\Scripts\activate.bat" Exit /B 1

call ./.venv/Scripts/activate.bat
