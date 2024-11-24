@echo off
REM This batch file will set up the environment by installing the necessary dependencies

echo Installing dependencies...

REM Ensure pip is installed
python -m ensurepip --upgrade

REM Install the required Python packages
pip install miniupnpc psutil requests

REM Create a file to verify that setup is complete
echo setup_complete > setup_complete.txt

echo Installation complete!
pause
