#!/bin/bash

# ClassMind Backend Startup Script

echo "🚀 Starting ClassMind Backend..."
echo ""

# Activate virtual environment
source venv/Scripts/activate

# Start uvicorn server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

echo ""
echo "✅ Backend server stopped"
