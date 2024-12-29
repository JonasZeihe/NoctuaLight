@echo off
echo Starting Noctua without logging...

rem !run_noctua.bat

rem Navigating to the src directory to ensure correct paths
cd /d "%~dp0src"

rem Setting PYTHONPATH to include the src directory if not already set
if not defined PYTHONPATH set PYTHONPATH=%~dp0src

rem Running the Noctua application without logging
python -m noctua.main

rem Pausing to allow review of any console output
pause
