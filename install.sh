#!/bin/bash
# Installation script for Expense Tracker Pro

echo "🚀 Expense Tracker Pro - Installation Script"
echo "============================================="
echo ""

# Check Python version
echo "📍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"
echo ""

# Create virtual environment
echo "📍 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "📍 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📍 Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install requirements
echo "📍 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📍 Creating directories..."
mkdir -p .streamlit
echo "✅ Directories created"
echo ""

# Copy config if needed
if [ ! -f ~/.streamlit/config.toml ]; then
    echo "📍 Setting up Streamlit configuration..."
    mkdir -p ~/.streamlit
    cp .streamlit/config.toml ~/.streamlit/
    echo "✅ Streamlit config installed"
else
    echo "⏭️  Streamlit config already exists"
fi
echo ""

echo "============================================="
echo "✨ Installation Complete!"
echo ""
echo "🚀 To start the application, run:"
echo "   streamlit run expense_tracker.py"
echo ""
echo "📱 The app will be available at:"
echo "   http://localhost:8501"
echo ""
echo "Happy Expense Tracking! 💰"