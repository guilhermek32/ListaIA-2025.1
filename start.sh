#!/bin/bash
# Startup script for Wine Recommendation System (Linux/Mac)

echo "================================"
echo "Wine Recommendation System"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "Please create .env file with PERPLEXITY_API_KEY"
    echo ""
fi

echo "Starting Backend API (Python)..."
echo ""
python api.py &
BACKEND_PID=$!

sleep 3

echo "Starting Frontend (Next.js)..."
echo ""
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "Both servers are running!"
echo "================================"
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend:    http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
