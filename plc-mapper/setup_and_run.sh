#!/bin/bash

# Setup and Run Script for PLC Data Mapping Assistant
# For Mac and Linux users

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     PLC Data Mapping Assistant - Setup & Run Script       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
echo "🔍 Checking for Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 is not installed!"
    echo "   Please install Python from: https://www.python.org/downloads/"
    exit 1
fi
echo ""

# Check if requirements are installed
echo "🔍 Checking dependencies..."
if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Dependencies already installed"
else
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi
echo ""

# Check for API key
echo "🔑 Checking for Anthropic API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  API key not found in environment"
    echo ""
    echo "You need an Anthropic API key to use this application."
    echo "Get one from: https://console.anthropic.com/"
    echo ""
    read -p "Do you have an API key? (y/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        read -p "Enter your Anthropic API key: " API_KEY
        export ANTHROPIC_API_KEY="$API_KEY"
        echo "✅ API key set for this session"
    else
        echo ""
        echo "Please get an API key from https://console.anthropic.com/"
        echo "Then run this script again."
        exit 1
    fi
else
    echo "✅ API key found: ${ANTHROPIC_API_KEY:0:20}..."
fi
echo ""

# Final check
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Ready to Launch! 🚀                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Starting the application..."
echo ""
echo "Once started, open your browser to:"
echo "  👉 http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server when done."
echo ""
echo "────────────────────────────────────────────────────────────"
echo ""

# Start the application
python3 app.py
