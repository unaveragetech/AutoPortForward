@echo off
REM This batch file will set up the environment by installing the necessary dependencies

echo Installing dependencies...

REM Ensure pip is installed
python -m ensurepip --upgrade

REM Install the required Python packages
pip install miniupnpc psutil requests

echo Installation complete!
pause
