#!/bin/bash
echo "Starting AlgoPrep Platform..."

# Start backend
echo "→ Starting FastAPI backend on :8000"
cd "$(dirname "$0")/backend"
python3 -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "→ Starting React frontend on :5173"
cd "$(dirname "$0")/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✓ Backend: http://localhost:8000/docs"
echo "✓ Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
