# 📊 Data Framework Performance Benchmark

A comprehensive benchmarking application that compares the performance of three popular Python data frameworks: **Dataclasses**, **Pydantic**, and **msgspec**. This project provides real-time performance analysis with a modern web interface.

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **API Endpoints**: RESTful endpoints for benchmarking operations
- **Models**: Implementations using dataclasses, Pydantic, and msgspec
- **Benchmarking**: Comprehensive performance testing utilities
- **Port**: 8000

### Frontend (Streamlit)
- **Framework**: Streamlit for interactive web interface
- **Components**: Modular UI components for benchmarking and visualization
- **Real-time**: Live performance metrics and visualization
- **Port**: 8501

### What They Achieve Together
The frontend provides an intuitive interface where users can configure benchmark parameters (number of objects, iterations) and view real-time performance comparisons. The backend handles the heavy computational work, running benchmarks for each framework and returning detailed metrics. Together, they create a complete benchmarking solution that demonstrates the performance trade-offs between different Python data frameworks.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites**: Docker and Docker Compose installed

**First-time setup:**
```bash
# Make shell scripts executable (run this once)
chmod +x *.sh
```

**Usage:**
```bash
# Start the entire application with one command
./start_app.sh

# Stop the entire application
./stop_app.sh

# Or use docker-compose directly
docker-compose up --build
docker-compose down
```

**Access the application:**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Option 2: Local Development

**Prerequisites**: Python 3.11+

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Backend (Terminal 1):**
   ```bash
   python backend/main.py
   ```

3. **Start Frontend (Terminal 2):**
   ```bash
   streamlit run frontend/main.py
   ```

### Option 3: Individual Services

```bash
# Start services
./start_backend.sh    # Start backend only
./start_frontend.sh   # Start frontend only

# Stop services
./stop_backend.sh     # Stop backend only
./stop_frontend.sh    # Stop frontend only
```

## 🎯 Features

### Data Frameworks Compared:
- **🐍 Dataclasses**: Python's built-in data class decorator (Python 3.7+)
- **✅ Pydantic**: Data validation and settings management using Python type annotations
- **⚡ msgspec**: A fast serialization and validation library

### Benchmark Types:
- **⚡ Quick Benchmark**: 100 objects × 5 iterations (fast test)
- **🔄 Full Benchmark**: Custom objects × iterations (comprehensive)
- **⚡🔄 Parallel Benchmark**: Same as full but runs frameworks in parallel (faster)

### Metrics Compared:
- **Instantiation Time**: Creating objects from dictionary data
- **Serialization Time**: Converting objects to JSON bytes
- **Deserialization Time**: Converting JSON bytes back to objects
- **Memory Usage**: Size of serialized data in bytes

### Visualizations:
- Performance comparison bar charts
- Memory usage analysis
- Radar chart showing overall performance
- Winners summary for each metric
- Real-time benchmark progress

## 🔧 Technical Details

### Backend Architecture:
- **FastAPI**: Modern, fast web framework for building APIs
- **Async Support**: Non-blocking operations for better performance
- **CORS Enabled**: Cross-origin requests for frontend communication
- **Health Check**: Endpoint for monitoring service status
- **Modular Design**: Separate modules for models, routes, and utilities

### Frontend Features:
- **Streamlit**: Interactive web applications with minimal code
- **Real-time Updates**: Live progress tracking during benchmarks
- **API Connection**: Automatic backend connectivity testing
- **Parameter Control**: Slider controls for benchmark configuration
- **Results Export**: Download benchmark results as CSV

### How Backend Works:
1. **Data Generation**: Creates random user data with realistic fields (id, name, email, age, is_active)
2. **Model Instantiation**: Converts dictionary data to framework-specific objects
3. **Serialization**: Transforms objects into JSON byte format
4. **Deserialization**: Reconstructs objects from JSON bytes
5. **Measurement**: Records timing and memory usage for each operation
6. **Aggregation**: Compiles results across multiple iterations for statistical accuracy

### How Frontend Works:
1. **Configuration Interface**: Sliders and inputs for benchmark parameters
2. **API Communication**: RESTful calls to backend endpoints
3. **Progress Tracking**: Real-time updates during benchmark execution
4. **Data Visualization**: Interactive charts using Plotly and Streamlit
5. **Results Analysis**: Comparative analysis with winner determination

## 📊 Expected Results

Performance characteristics you should typically observe:

- **🏆 msgspec**: 
  - **Fastest**: Serialization and deserialization
  - **Smallest**: Memory footprint for simple data
  - **Best for**: High-performance applications, APIs

- **🛡️ Pydantic**: 
  - **Strongest**: Data validation and error handling
  - **Most Features**: Rich ecosystem and integrations
  - **Best for**: Data APIs, configuration management

- **🐍 Dataclasses**: 
  - **Simplest**: Minimal overhead, standard library
  - **Most Compatible**: No external dependencies
  - **Best for**: Simple data containers, legacy systems

## 🐳 Docker Support

This project includes full Docker support with:

- **Multi-service Architecture**: Separate containers for frontend and backend
- **Health Checks**: Automatic service monitoring
- **Development Mode**: Hot reload for code changes
- **Network Isolation**: Internal Docker networking
- **Volume Mounts**: Persistent data and code updates

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

## 🎓 Perfect for Academic Presentations!

- Clean, professional interface
- Clear performance metrics
- Visual comparisons with interactive charts
- Real-time benchmarking with progress indicators
- Comprehensive error handling and timeouts
- Educational value demonstrating framework trade-offs
- Easy to reproduce results across different environments

## 📁 Project Structure

```
Project/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Application entry point
│   ├── models/             # Data model implementations
│   │   ├── dataclass_model.py
│   │   ├── pydantic_model.py
│   │   └── msgspec_model.py
│   ├── routes/             # API route handlers
│   │   └── benchmark.py
│   └── utils/              # Utilities
│       ├── benchmarking.py
│       └── data_generator.py
├── frontend/               # Streamlit Frontend
│   ├── main.py            # Application entry point
│   └── components/        # UI components
│       ├── benchmark_ui.py
│       └── results_viz.py
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Multi-service orchestration
├── start_app.sh         # Start full application
├── start_backend.sh     # Start backend only
├── start_frontend.sh    # Start frontend only
├── stop_app.sh          # Stop full application
├── stop_backend.sh      # Stop backend only
├── stop_frontend.sh     # Stop frontend only
├── README.md           # This file
└── DOCKER.md          # Docker documentation
```

## 🔄 API Endpoints

### Backend API (FastAPI)
- `GET /health` - Health check endpoint
- `POST /api/benchmark/quick` - Run quick benchmark
- `POST /api/benchmark/full` - Run comprehensive benchmark
- `POST /api/benchmark/parallel` - Run parallel benchmark
- `GET /docs` - Interactive API documentation (Swagger UI)

## 🛠️ Development

### Local Development Setup
```bash
# Clone and navigate to project
git clone <repository-url>
cd Project

# Make scripts executable (first time only)
chmod +x *.sh

# Install dependencies
pip install -r requirements.txt

# Start backend (development mode)
cd backend && python main.py

# Start frontend (new terminal)
streamlit run frontend/main.py
```

### Making Executable Scripts
If you get permission denied errors when running shell scripts:
```bash
# Make all shell scripts executable
chmod +x *.sh

# Or individually
chmod +x start_app.sh start_backend.sh start_frontend.sh
chmod +x stop_app.sh stop_backend.sh stop_frontend.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker: `docker-compose up --build`
5. Submit a pull request

## 📄 License

This project is for educational purposes and academic presentations.

## 🎯 Use Cases

- **Academic Research**: Compare data framework performance
- **Technology Evaluation**: Choose the right framework for your project
- **Educational Tool**: Learn about Python data frameworks
- **Performance Analysis**: Understand trade-offs between frameworks
- **Presentation Tool**: Demonstrate framework differences in real-time