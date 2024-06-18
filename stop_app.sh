#!/bin/bash

if [ -f frontend.pid ]; then
    echo "Killing frontend process..."
    kill $(cat frontend.pid)
    rm frontend.pid  # Remove the PID file
else
    echo "Frontend process not found."
fi

if [ -f backend/app/backend.pid ]; then
    echo "Killing backend process..."
    kill $(cat backend/app/backend.pid)
    rm backend/app/backend.pid  # Remove the PID file
else
    echo "Backend process not found."
fi
