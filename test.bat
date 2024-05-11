@echo off

::Activate the virtual environment
call ./.venv/Scripts/activate.bat

cd /d %~dp0\src\tests\

python -m unittest discover

cd /d %~dp0\

:: Deactivate the virtual environment
call ./.venv/Scripts/deactivate.bat


