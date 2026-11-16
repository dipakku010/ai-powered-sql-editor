#!/bin/bash
# Quick Start Script for AI SQL Editor (Streamlit + Flask)
# This script helps you run both the Flask API and Streamlit UI

echo "=================================="
echo "AI SQL Editor - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Get the workspace directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_DIR="$SCRIPT_DIR/workspace"

echo "📁 Working directory: $SCRIPT_DIR"
echo "📁 Flask workspace: $WORKSPACE_DIR"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit; import flask; import requests; import langchain_groq" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Installing..."
    pip3 install -r "$SCRIPT_DIR/requirements.txt" 2>&1 | tail -5
    echo "✅ Dependencies installed"
else
    echo "✅ All dependencies are installed"
fi

echo ""
echo "=================================="
echo "Starting Services..."
echo "=================================="
echo ""

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  GROQ_API_KEY environment variable is not set"
    echo "   The Flask API may fail if Groq LLM is not configured"
    echo ""
fi

# Start Flask in background
echo "🚀 Starting Flask API on http://127.0.0.1:5002..."
cd "$WORKSPACE_DIR"
python3 flask_app.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 3

# Check if Flask is running
if ! kill -0 $FLASK_PID 2>/dev/null; then
    echo "❌ Failed to start Flask API"
    exit 1
fi

echo "✅ Flask API started (PID: $FLASK_PID)"
echo ""

# Start Streamlit
echo "🎨 Starting Streamlit UI on http://localhost:8501..."
echo ""
cd "$SCRIPT_DIR"
python3 -m streamlit run streamlit_ui.py

# Cleanup on exit
echo ""
echo "Shutting down..."
kill $FLASK_PID 2>/dev/null
echo "✅ Done"
