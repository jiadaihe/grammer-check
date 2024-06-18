#!/bin/bash

# Start the frontend
echo "Starting frontend..."
nohup npm start > frontend.log 2>&1 &
echo $! > frontend.pid  # Store frontend PID
sleep 5

# Start the backend
echo "Starting backend..."
cd backend/app
nohup uvicorn server:app --reload > backend.log 2>&1 &
echo $! > backend.pid  # Store backend PID
