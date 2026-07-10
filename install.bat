@echo off
REM Installation script for Expense Tracker Pro (Windows)

echo.
echo 🚀 Expense Tracker Pro - Installation Script (Windows)
echo ======================================================
echo.

REM Check Python version
echo 📍 Checking Python version...
python --version
echo ✅ Python found
echo.

REM Create virtual environment
echo 📍 Creating virtual environment...
python -m venv venv
echo ✅ Virtual environment created
echo.

REM Activate virtual environment
echo 📍 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo 📍 Upgrading pip...
python -m pip install --upgrade pip
echo ✅ pip upgraded
echo.

REM Install requirements
echo 📍 Installing dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Create necessary directories
echo 📍 Creating directories...
if not exist ".streamlit" mkdir .streamlit
echo ✅ Directories created
echo.

echo ======================================================
echo ✨ Installation Complete!
echo.
echo 🚀 To start the application, run:
echo    streamlit run expense_tracker.py
echo.
echo 📱 The app will be available at:
echo    http://localhost:8501
echo.
echo Happy Expense Tracking! 💰
echo.
pause
