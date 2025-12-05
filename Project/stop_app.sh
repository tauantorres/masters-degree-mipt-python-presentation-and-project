#!/bin/bash

# Stop Full Application Script for Data Framework Benchmark
# This script stops both backend and frontend services

set -e

echo "🛑 Stopping Data Framework Benchmark Application..."
echo "================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running or not accessible."
    exit 1
fi

# Stop all services
echo "🔨 Stopping all services..."
docker-compose down

echo "✅ Application stopped successfully!"
echo ""
echo "ℹ️  To remove all containers, networks, and volumes, run:"
echo "   docker-compose down -v"
echo ""
echo "ℹ️  To remove containers, networks, volumes, and images, run:"
echo "   docker-compose down -v --rmi all"