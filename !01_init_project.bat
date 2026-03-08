@echo off
REM ----------------------------------------------------------------------
REM Universal Project Initializer
REM Initializes a virtual environment and installs dependencies.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Check if the virtual environment already exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Inform the user
echo Virtual environment setup complete!
echo Press any key to deactivate the virtual environment and exit...
pause > nul

REM Deactivate the virtual environment
deactivate
