#!/bin/bash

# Start Frontend Script for Data Framework Benchmark
# This script starts the Streamlit frontend service

set -e

echo "🖥️  Starting Data Framework Benchmark Frontend..."
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if backend is running
if ! docker-compose ps | grep -q "benchmark_backend.*Up"; then
    echo "⚠️  Backend is not running. Starting backend first..."
    docker-compose up -d backend
    
    echo "⏳ Waiting for backend to be ready..."
    sleep 10
fi

# Build and start frontend service
echo "🔨 Building and starting frontend service..."
docker-compose up --build frontend

echo "✅ Frontend started successfully!"
echo "🌐 Frontend is available at: http://localhost:8501"
echo ""
echo "To stop the frontend, press Ctrl+C or run:"
echo "docker-compose down"