@echo off
REM ----------------------------------------------------------------------
REM Update Requirements Script
REM Generates or updates the requirements.txt file based on the active virtual environment.
REM 
REM Copyright (c) 2024 Jonas Zeihe 
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra 
REM Contact: JonasZeihe@gmail.com 
REM ----------------------------------------------------------------------

@echo off
cls

REM Check if the virtual environment exists
if not exist "venv\Scripts\activate" (
    echo Virtual environment not found! Please initialize the project first.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Generate or update requirements.txt
echo Updating requirements.txt...
pip freeze > requirements.txt


REM Inform the user
echo.
echo requirements.txt has been updated successfully.
echo Press any key to deactivate the virtual environment and close this window...
pause > nul

REM Deactivate the virtual environment
deactivate
