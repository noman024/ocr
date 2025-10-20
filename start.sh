#!/bin/bash

# Get port from environment variable or use default
PORT=${PORT:-8080}

# Start the application
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
