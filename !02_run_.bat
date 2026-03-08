@echo off
REM ----------------------------------------------------------------------
REM Universal Application Runner
REM Runs the application within the virtual environment, allowing drag-and-drop for input files.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/skryper
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Activate the virtual environment
call venv\Scripts\activate

REM Set PYTHONPATH to include the src directory
set PYTHONPATH=%~dp0src

REM Run the application with the provided file(s)
echo Running the application...
python src/noctua/main.py %*

REM Inform the user
echo Application execution complete. Press any key to deactivate the virtual environment and exit...
pause > nul

REM Deactivate the virtual environment
deactivate
