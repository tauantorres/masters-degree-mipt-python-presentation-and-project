#!/bin/bash

# Stop Frontend Script for Data Framework Benchmark
# This script stops only the Streamlit frontend service

set -e

echo "🛑 Stopping Data Framework Benchmark Frontend..."
echo "==========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running or not accessible."
    exit 1
fi

# Stop frontend service
echo "🔨 Stopping frontend service..."
docker-compose stop frontend

echo "✅ Frontend stopped successfully!"
echo ""
echo "ℹ️  To restart the frontend, run:"
echo "   ./start_frontend.sh"
echo ""
echo "ℹ️  To completely remove the frontend container, run:"
echo "   docker-compose rm frontend"