# Docker Setup for Data Framework Benchmark

This document explains how to build and run the Data Framework Benchmark application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the applications:**
   - **Frontend (Streamlit):** http://localhost:8501
   - **Backend (FastAPI):** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs

3. **Stop the services:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Shell Scripts

Use the provided shell scripts for easier management:

```bash
# Start the entire application (backend + frontend)
./start_app.sh

# Stop the entire application
./stop_app.sh

# Or manage services individually
./start_backend.sh    # Start backend only
./start_frontend.sh   # Start frontend only
./stop_backend.sh     # Stop backend only
./stop_frontend.sh    # Stop frontend only
```

## Docker Commands

### Building the Image
```bash
# Build the Docker image
docker-compose build

# Or build without cache
docker-compose build --no-cache
```

### Running Services
```bash
# Start in background (detached mode)
docker-compose up -d

# Start with logs visible
docker-compose up

# Start specific service
docker-compose up backend
docker-compose up frontend
```

### Monitoring and Debugging
```bash
# View logs
docker-compose logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f

# Check running containers
docker-compose ps

# Execute commands in running container
docker-compose exec backend bash
docker-compose exec frontend bash
```

### Cleanup
```bash
# Stop and remove containers
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove containers, networks, volumes, and images
docker-compose down -v --rmi all
```

## Architecture

The Docker setup consists of:

- **Backend Service**: FastAPI application running on port 8000
- **Frontend Service**: Streamlit application running on port 8501
- **Network**: Custom bridge network for inter-service communication
- **Volumes**: Shared volume for application data

## Environment Variables

- `DOCKER_ENV=1`: Indicates the application is running in Docker
- Backend runs on `0.0.0.0:8000`
- Frontend runs on `0.0.0.0:8501`

## Health Checks

The backend service includes health checks that:
- Test the `/health` endpoint every 30 seconds
- Wait 40 seconds before starting health checks
- Retry 3 times with 10-second timeout

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using the port
   lsof -i :8000
   lsof -i :8501
   
   # Kill process using the port
   kill -9 <PID>
   ```

2. **Permission denied:**
   ```bash
   # Make scripts executable
   chmod +x start_app.sh start_backend.sh start_frontend.sh
   ```

3. **Build failures:**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

4. **Services not communicating:**
   - Check if both services are on the same network
   - Verify environment variables are set correctly
   - Check firewall settings

### Logs and Debugging

- Check container logs: `docker-compose logs <service_name>`
- Access container shell: `docker-compose exec <service_name> bash`
- Monitor resource usage: `docker stats`

## Development Mode

For development, the containers are set up with volume mounts, so code changes are reflected immediately without rebuilding the image.

```bash
# Start in development mode with logs
docker-compose up

# The application will auto-reload when files change
```