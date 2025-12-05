#!/bin/bash

# Stop Backend Script for Data Framework Benchmark
# This script stops only the FastAPI backend service

set -e

echo "🛑 Stopping Data Framework Benchmark Backend..."
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running or not accessible."
    exit 1
fi

# Stop backend service
echo "🔨 Stopping backend service..."
docker-compose stop backend

echo "✅ Backend stopped successfully!"
echo ""
echo "ℹ️  To restart the backend, run:"
echo "   ./start_backend.sh"
echo ""
echo "ℹ️  To completely remove the backend container, run:"
echo "   docker-compose rm backend"