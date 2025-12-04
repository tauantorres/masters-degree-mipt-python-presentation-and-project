import json
import requests
import streamlit as st
from typing import Self, List, Dict, Any, Optional 


class BenchmarkUI:

    def __init__(self: Self, api_url: str) -> None:
        self.api_url = api_url.rstrip('/')

    def run_benchmark(
        self: Self,
        batch_size: int,
        iterations: int,
        timeout: int = 240
    ) -> Optional[Dict[str, Any]]:
        try:
            st.info(f"🚀 Starting benchmark: {batch_size} objects × {iterations} iterations...")

            response = requests.post(
                url=f"{self.api_url}/api/benchmark/run",
                params={
                    'batch_size': batch_size,
                    'iterations': iterations
                },
                timeout=timeout,
            )

            if response.status_code == 200:
                return response.json()
            else:
                response_dict: dict = response.json()
                error_detail = response_dict.get('detail', 'Unknown error') if response.content else 'No response from server'
                st.error(f"❌ Benchmark failed: {error_detail}")
                return None

        except requests.exceptions.Timeout:
            st.error("⏰ Benchmark timed out. Try reducing the number of objects or iterations.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection failed. Please check if the backend is running.")
            return None
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
        
    def run_benchmark_parallel(
        self: Self,
        batch_size: int,
        iterations: int,
        timeout: int = 300
    ) -> Optional[Dict[str, Any]]:

        try:
            st.info(f"🚀 Starting parallel benchmark: {batch_size} objects × {iterations} iterations...")

            response = requests.post(
                url=f"{self.api_url}/api/benchmark/run-parallel",
                params={
                    'batch_size': batch_size,
                    'iterations': iterations
                },
                timeout=timeout,
            )

            if response.status_code == 200:
                return response.json()
            else:
                response_dict: dict = response.json()
                error_detail = response_dict.get('detail', 'Unknown error') if response.content else 'No response from server'
                st.error(f"❌ Parallel benchmark failed: {error_detail}")
                return None

        except requests.exceptions.Timeout:
            st.error("⏰ Parallel benchmark timed out. Try reducing the number of objects or iterations.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection failed. Please check if the backend is running.")
            return None
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
        
    def run_quick_benchmark(self: Self, timeout: int = 60) -> Optional[Dict[str, Any]]:
        try:
            st.info("⚡ Running quick benchmark with 100 objects and 5 iterations...")
            
            response = requests.get(f"{self.api_url}/api/benchmark/quick", timeout=timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                response_dict: dict = response.json()
                error_detail = response_dict.get('detail', 'Unknown error') if response.content else 'No response from server'
                st.error(f"❌ Quick benchmark failed: {error_detail}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏰ Quick benchmark timed out. The backend might be overloaded.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection failed. Please check if the backend is running.")
            return None  
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
        
    def get_frameworks(self: Self, timeout: int = 30) -> Optional[List[str]]:
        try:
            response = requests.get(f"{self.api_url}/api/benchmark/frameworks", timeout=timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                response_dict: dict = response.json()
                error_detail = response_dict.get('detail', 'Unknown error') if response.content else 'No response from server'
                st.error(f"❌ Failed to get frameworks: {error_detail}")
                return None

        except requests.exceptions.Timeout:
            st.error("⏰ Request for frameworks timed out.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection failed. Please check if the backend is running.")
            return None  
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
    
    def display_frameworks_info(self: Self, frameworks: List[Dict[str, Any]]) -> None:
        st.subheader("🔧 Available Frameworks")
        for framework in frameworks:
            with st.expander(f"📚 {framework.get('name', 'Unknown Framework')}"):
                column_1, column_2 = st.columns([2, 1])
                
                with column_1:
                    st.markdown(f"**Description:** {framework.get('description', 'No description available.')}")
                    st.markdown(f"**Version:** {framework.get('version', 'N/A')}")
                
                with column_2:
                    st.markdown("**Features:**")
                    for feature in framework.get('features', []):
                        st.markdown(f"• {feature}")

