#!/bin/bash

# OCR API Local Deployment Script with ngrok
# Usage: ./deploy.sh [PORT]

set -e

# Default values
PORT=${1:-8080}

echo "🚀 Deploying OCR API locally with ngrok"
echo "Port: $PORT"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not found. Please install it first:"
    echo "   - Download from: https://ngrok.com/download"
    echo "   - Or install via: sudo snap install ngrok"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract not found. Please install it first:"
    echo "   sudo apt-get install tesseract-ocr tesseract-ocr-eng"
    exit 1
fi

echo "✅ Tesseract found: $(tesseract --version | head -n1)"

# Start the API server in background
echo "🚀 Starting API server on port $PORT..."
source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if ! curl -s http://localhost:$PORT/health > /dev/null; then
    echo "❌ Failed to start API server"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "✅ API server started successfully"

# Start ngrok tunnel
echo "🌐 Starting ngrok tunnel..."
ngrok http $PORT &
NGROK_PID=$!

# Wait for ngrok to start
sleep 5

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tunnel in data['tunnels']:
    if tunnel['proto'] == 'https':
        print(tunnel['public_url'])
        break
")

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL"
    kill $SERVER_PID $NGROK_PID 2>/dev/null
    exit 1
fi

echo "✅ Deployment completed!"
echo "🌐 Public URL: $NGROK_URL"
echo ""
echo "🧪 Test your API:"
echo "curl -X POST -F \"image=@sample_images/text_sample.jpg\" $NGROK_URL/extract-text"
echo ""
echo "📊 Health check:"
echo "curl $NGROK_URL/health"
echo ""
echo "🛑 To stop the services:"
echo "kill $SERVER_PID $NGROK_PID"
