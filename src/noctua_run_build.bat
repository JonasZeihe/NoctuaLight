@echo off
REM ---------------------------------------------------------------------------
REM Noctua - A tool to scan and report hardware configurations
REM 
REM Copyright (c) 2024
REM Licensed under the MIT License. See LICENSE file in the project root.
REM ---------------------------------------------------------------------------

rem noctua_run_build.bat

cls
REM Set the working directory to the project root (no need to change to src)
cd /d %~dp0

REM Clean previous build directories, but only if they exist
echo Cleaning previous builds...
if exist build rd /s /q build
if exist dist rd /s /q dist

REM Building the Noctua executable with PyInstaller
echo Building Noctua executable...
pyinstaller --name noctua --onefile --add-data "C:\\dev\\repos\\noctua\\resources\\images;resources/images" --specpath . --noconfirm noctua/main.py

REM Check if PyInstaller was successful
if %errorlevel% neq 0 (
    echo.
    echo Build failed. Please check the errors above.
    echo Press any key to exit...
    pause > nul
    exit /b %errorlevel%
)

REM Move to the dist directory if build was successful
cd dist

REM Show build result
echo.
echo Build complete. The executable can be found in the 'dist' folder.
echo Press any key to exit...
pause > nul
