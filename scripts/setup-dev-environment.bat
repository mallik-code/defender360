@echo off
REM Development Environment Setup Script for Windows
REM Sets up the complete development environment for the Agentic SOC Framework.

echo Starting Agentic SOC Framework development environment setup...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.12+
    echo See docs/development/installation-guides/windows-setup.md
    exit /b 1
)

REM Run the Python setup script
python scripts/setup-dev-environment.py
exit /b %errorlevel%