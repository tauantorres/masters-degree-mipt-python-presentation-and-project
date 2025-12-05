#!/bin/bash

# Start Full Application Script for Data Framework Benchmark
# This script starts both backend and frontend services

set -e

echo "🚀 Starting Data Framework Benchmark Application..."
echo "================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start all services
echo "🔨 Building and starting all services..."
docker-compose up --build

echo "✅ Application started successfully!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend (Streamlit): http://localhost:8501"
echo "   Backend (FastAPI):    http://localhost:8000"
echo "   API Documentation:    http://localhost:8000/docs"
echo ""
echo "To stop the application, press Ctrl+C or run:"
echo "docker-compose down"