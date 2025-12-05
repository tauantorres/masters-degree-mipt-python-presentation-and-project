#!/bin/bash

# Start Backend Script for Data Framework Benchmark
# This script starts the FastAPI backend service

set -e

echo "🚀 Starting Data Framework Benchmark Backend..."
echo "====================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start backend service
echo "🔨 Building and starting backend service..."
docker-compose up --build backend

echo "✅ Backend started successfully!"
echo "🌐 Backend is available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the backend, press Ctrl+C or run:"
echo "docker-compose down"