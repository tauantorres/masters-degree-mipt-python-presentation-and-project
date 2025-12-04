#!/bin/bash
cd "$(dirname "$0")/backend"
echo "🚀 Starting FastAPI Backend..."
echo "📍 API will be available at: http://127.0.0.1:8000"
echo "📍 API Documentation: http://127.0.0.1:8000/docs"
echo ""
fastapi dev main.py