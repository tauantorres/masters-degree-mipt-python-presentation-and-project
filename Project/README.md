# 📊 Data Framework Performance Benchmark

A simple, fast application comparing Python data frameworks: **Dataclasses**, **Pydantic**, and **msgspec**.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Backend dependencies (in your venv/conda environment)
pip install fastapi uvicorn msgspec pydantic

# Frontend dependencies
cd frontend
pip install -r requirements.txt
```

### 2. Start Backend (Terminal 1)
```bash
./start_backend.sh
```
Backend will be available at: http://127.0.0.1:8000

### 3. Start Frontend (Terminal 2)
```bash
./start_frontend.sh
```
Frontend will be available at: http://localhost:8501

## 🎯 Features

### Benchmark Types:
- **⚡ Quick Benchmark**: 100 objects × 5 iterations (fast test)
- **🔄 Full Benchmark**: Custom objects × iterations (comprehensive)
- **⚡🔄 Parallel Benchmark**: Same as full but runs frameworks in parallel (faster)

### Metrics Compared:
- **Instantiation Time**: Creating objects from dict data
- **Serialization Time**: Converting objects to JSON bytes
- **Deserialization Time**: Converting JSON bytes back to objects
- **Memory Usage**: Size of serialized data

### Visualizations:
- Performance comparison bar charts
- Memory usage analysis
- Radar chart showing overall performance
- Winners summary for each metric

## 📊 Expected Results

Generally, you should see:
- **msgspec**: Fastest serialization/deserialization
- **dataclasses**: Lowest memory overhead
- **Pydantic**: Best validation features (trade-off for speed)

## 🎓 Perfect for Academic Presentations!

- Clean, professional interface
- Clear performance metrics
- Visual comparisons
- Real-time benchmarking
- Error handling and timeouts