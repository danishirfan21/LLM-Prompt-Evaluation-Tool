#!/bin/bash

echo "🚀 LLM Evaluation Tool - Setup & Run"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env with your API keys"
    echo "See README.md for instructions"
    exit 1
fi

# Check for credentials.json
if [ ! -f "credentials.json" ]; then
    echo "⚠️  Warning: credentials.json not found!"
    echo "Please download Google service account credentials"
    echo "See README.md for instructions"
    exit 1
fi

# Check if templates directory exists
if [ ! -d "templates" ]; then
    echo "📁 Creating templates directory..."
    mkdir templates
    echo "⚠️  Please add index.html to templates/ directory"
fi

# Run the application
echo ""
echo "✨ Starting Flask application..."
echo "🌐 Open http://localhost:5000 in your browser"
echo ""
python app.py