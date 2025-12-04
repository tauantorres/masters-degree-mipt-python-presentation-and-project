#!/bin/bash
cd "$(dirname "$0")/frontend"
echo "🎯 Starting Streamlit Frontend..."
echo "📍 Frontend will be available at: http://localhost:8501"
echo ""
streamlit run main.py