import os
import streamlit as st
from components.results_viz import ResultsViz
from components.benchmark_ui import BenchmarkUI

# Page configuration
st.set_page_config(
    page_title="Data Framework Benchmark",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("📊 Data Framework Performance Benchmark")
st.markdown("""
This app compares the performance of different Python data frameworks:
- **Dataclasses** (Python standard library)
- **Pydantic** (Data validation and settings management)
- **msgspec** (Fast serialization library)
""")

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("Configure your benchmark parameters:")

# Initialize session state first (before any widgets)
if 'api_tested' not in st.session_state:
    st.session_state.api_tested = False
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = False
if 'benchmark_running' not in st.session_state:
    st.session_state.benchmark_running = False
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://127.0.0.1:8000"

# API URL configuration
api_url = st.sidebar.text_input(
    "API URL",
    value=st.session_state.api_url,
    key="api_url_input",
    help="Backend API URL"
)

# Update session state
st.session_state.api_url = api_url

# Test API connection
@st.cache_data(ttl=30)  # Cache for 30 seconds
def test_api_connection(url: str) -> bool:
    try:
        import requests
        response = requests.get(f"{url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Connection status
if not st.session_state.api_tested or st.session_state.get('last_api_url') != api_url:
    st.session_state.api_connected = test_api_connection(api_url)
    st.session_state.api_tested = True
    st.session_state.last_api_url = api_url

if st.session_state.api_connected:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Disconnected")
    st.error(f"Cannot connect to API at {api_url}. Please make sure the backend is running.")
    st.info("💡 **Troubleshooting:**\n- Check if the backend is running\n- Try refreshing the page\n- Verify the API URL is correct")
    st.stop()

# Initialize components
benchmark_ui = BenchmarkUI(api_url)
results_viz = ResultsViz()

# Main tabs
tab1, tab2 = st.tabs(["🚀 Benchmark", "📈 Results Analysis"])

with tab1:
    st.header("🚀 Run Benchmarks")
    
    # Benchmark parameters
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.slider(
            "Number of objects",
            min_value=10,
            max_value=10000,
            value=1000,
            step=10,
            help="Number of data objects to create and serialize"
        )
    
    with col2:
        iterations = st.slider(
            "Iterations",
            min_value=1,
            max_value=50,
            value=10,
            help="Number of iterations for more accurate timing"
        )
    
    # Benchmark buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⚡ Quick Benchmark", disabled=st.session_state.benchmark_running, width="stretch"):
            if not st.session_state.benchmark_running:
                st.session_state.benchmark_running = True
                with st.spinner("Running quick benchmark..."):
                    results = benchmark_ui.run_quick_benchmark()
                    if results:
                        st.session_state.last_results = results
                        st.success("✅ Quick benchmark completed!")
                    else:
                        st.error("❌ Quick benchmark failed")
                st.session_state.benchmark_running = False
                st.rerun()
    
    with col2:
        if st.button("🔄 Full Benchmark", disabled=st.session_state.benchmark_running, width="stretch"):
            if not st.session_state.benchmark_running:
                st.session_state.benchmark_running = True
                with st.spinner(f"Running full benchmark with {batch_size} objects..."):
                    results = benchmark_ui.run_benchmark(batch_size, iterations)
                    if results:
                        st.session_state.last_results = results
                        st.success("✅ Full benchmark completed!")
                    else:
                        st.error("❌ Full benchmark failed")
                st.session_state.benchmark_running = False
                st.rerun()
    
    with col3:
        if st.button("⚡🔄 Parallel Benchmark", disabled=st.session_state.benchmark_running, width="stretch"):
            if not st.session_state.benchmark_running:
                st.session_state.benchmark_running = True
                with st.spinner(f"Running parallel benchmark with {batch_size} objects..."):
                    results = benchmark_ui.run_benchmark_parallel(batch_size, iterations)
                    if results:
                        st.session_state.last_results = results
                        st.success("✅ Parallel benchmark completed!")
                    else:
                        st.error("❌ Parallel benchmark failed")
                st.session_state.benchmark_running = False
                st.rerun()
    
    with col4:
        if st.button("🗑️ Clear Results", width="stretch"):
            if 'last_results' in st.session_state:
                del st.session_state.last_results
                st.success("✅ Results cleared!")
                st.rerun()
    
    # Display benchmark status
    if st.session_state.benchmark_running:
        st.info("⏳ Benchmark in progress... Please wait and do not refresh the page.")
    
    # Display latest results
    if 'last_results' in st.session_state and not st.session_state.benchmark_running:
        try:
            st.divider()
            st.subheader("📊 Latest Benchmark Results")
            results_viz.display_results(st.session_state.last_results)
        except Exception as e:
            st.error(f"Error displaying results: {str(e)}")
            st.write("Debug - results data:", st.session_state.last_results)

with tab2:
    st.header("📈 Results Analysis")
    
    if 'last_results' in st.session_state:
        results_viz.display_results(st.session_state.last_results)
    else:
        st.info("🎯 Run a benchmark first to see detailed analysis here!")
        
        # Show framework information
        with st.expander("📚 Framework Information"):
            st.markdown("""
            ### Dataclasses
            - **Type**: Python standard library (3.7+)
            - **Features**: Type hints, automatic methods, immutability option
            - **Best for**: Simple data structures without validation
            
            ### Pydantic
            - **Type**: Third-party validation library (v2.x)
            - **Features**: Data validation, JSON schema, FastAPI integration
            - **Best for**: APIs requiring data validation and serialization
            
            ### msgspec
            - **Type**: High-performance serialization library (0.18+)
            - **Features**: Multiple formats, schema validation, extreme speed
            - **Best for**: High-performance applications requiring fast serialization
            """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    🐍 Built with FastAPI + Streamlit | 
    📊 Comparing Dataclasses vs Pydantic vs msgspec
</div>
""", unsafe_allow_html=True)

