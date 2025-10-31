#!/bin/bash

# Quick start script for PLC Mapping Assistant

echo "PLC Data Mapping Assistant - Quick Start"
echo "========================================"
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY environment variable is not set!"
    echo ""
    echo "Please set your API key before running:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting Flask server..."
echo "Open http://localhost:5000 in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
