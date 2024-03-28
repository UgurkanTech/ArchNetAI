@echo off
If Not Exist ".venv\Scripts\activate.bat" (
    pip install virtualenv
    python -m venv .venv
)

If Not Exist ".venv\Scripts\activate.bat" Exit /B 1

call ./.venv/Scripts/activate.bat

:: Visual Studio Build tools - Desktop development with C++ required

set FORCE_CMAKE=1
set CMAKE_ARGS=-DLLAMA_CUBLAS=on

pip install -r requirements.txt  --force-reinstall --upgrade --no-cache-dir
