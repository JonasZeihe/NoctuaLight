@echo off
echo Starting Noctua with logging...

rem !run_noctua_logging.bat

rem Navigating to the src directory to ensure correct paths
cd /d "%~dp0src"

rem Setting PYTHONPATH to include the src directory if not already set
if not defined PYTHONPATH set PYTHONPATH=%~dp0src

rem Running the Noctua application with logging enabled
python -m noctua.main --logging

rem Pausing to allow review of any console output
pause
