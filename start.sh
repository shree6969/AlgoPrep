#!/bin/bash
ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "Starting AlgoPrep Platform..."

# Kill anything already on these ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Start backend
echo "→ Starting FastAPI backend on :8000"
cd "$ROOT/backend"
python3 -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "→ Starting React frontend on :5173"
cd "$ROOT/frontend"
node node_modules/vite/bin/vite.js &
FRONTEND_PID=$!

echo ""
echo "✓ Backend: http://localhost:8000/docs"
echo "✓ Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
