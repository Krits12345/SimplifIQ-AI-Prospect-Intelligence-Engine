#!/bin/bash

# SimplifIQ Backend Startup Script
# This script initializes the database and starts the FastAPI server

set -e

echo "🚀 Starting SimplifIQ AI Prospect Intelligence Backend"
echo "=================================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example"
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your API keys."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Virtual environment created and dependencies installed"
else
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Create reports directory if it doesn't exist
if [ ! -d "reports" ]; then
    echo "📁 Creating reports directory..."
    mkdir reports
fi

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from app.database import init_db; init_db()"
echo "✅ Database initialized"

# Start the server
echo ""
echo "🌐 Starting FastAPI server..."
echo "📍 Backend URL: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
