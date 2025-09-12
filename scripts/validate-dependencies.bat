@echo off
REM Dependency Validation Script for Windows
REM Validates system dependencies and requirements for local development.

echo Starting Agentic SOC Framework dependency validation...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.12+
    echo See docs/development/installation-guides/windows-setup.md
    exit /b 1
)

REM Run the Python validation script
python scripts/validate-dependencies.py
exit /b %errorlevel%