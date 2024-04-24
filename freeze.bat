@echo off

REM Check if the virtual environment exists
if not exist ".venv\Scripts\activate" (
    echo Virtual environment does not exist. Please run setup.bat first.
    exit /b 1
)

REM Activate the virtual environment
call .venv\Scripts\activate

if exist "requirements.txt" (
    echo requirements.txt already exists. Installing..
    set FORCE_CMAKE=1
    set CMAKE_ARGS=-DLLAMA_CUBLAS=on
    pip install -r requirements.txt  --force-reinstall --upgrade --no-cache-dir
    echo requirements.txt installed successfully.
) else (
    echo requirements.txt does not exist. Creating one with .venv libraries...
    pip freeze > requirements.txt
    echo requirements.txt created successfully.
)