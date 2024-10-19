#!/bin/bash

# This script starts the AI Backend Wrapper MVP.

set -e

echo "Starting AI Backend Wrapper MVP..."

# Source the environment variables.
if [ -f .env ]; then
  source .env
fi

# Start the backend application.
echo "Starting backend..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &

# Wait for the backend to start.
sleep 5

# Check if the backend is running.
if ! ps aux | grep -q 'uvicorn api.main:app'; then
  echo "Error: Backend failed to start."
  exit 1
fi

echo "Backend started successfully."

# Optional: Start the database (if applicable).
# echo "Starting database..."
# docker-compose up -d database &
# sleep 5
# if ! docker-compose ps | grep -q 'database'; then
#   echo "Error: Database failed to start."
#   exit 1
# fi
# echo "Database started successfully."

echo "AI Backend Wrapper MVP started successfully."