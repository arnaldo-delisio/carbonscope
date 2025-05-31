#!/bin/bash

# CarbonScope Development Startup Script

echo "🚀 Starting CarbonScope Development Environment"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Please run this from the project root directory"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "   Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "   Installing dependencies..."
pip install -r requirements.txt

# Start backend
echo "   Starting backend server..."
echo "   Backend will be available at: http://localhost:8000"
echo "   API documentation: http://localhost:8000/docs"
echo ""

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
