import json
import requests
import pandas as pd
import streamlit as st
from typing import Self, List, Dict, Any, Optional

import plotly.express as px
import plotly.graph_objects as go


class ResultsViz:
    
    def __init__(self: Self) -> None:
        pass

    def display_results(self: Self, results: Dict[str, Any], key_prefix: str = "") -> None:

        if 'results' not in results:
            st.error("No results to display.")
            return
        
        params: dict = results.get('parameters', {})

        col1, col2= st.columns(2)

        with col1:
            st.metric("Objects", value=params.get('batch_size', 'N/A'))
        with col2:
            st.metric("Iterations", value=params.get('iterations', 'N/A'))
        st.markdown("---")

        self._create_performance_charts(results=results.get('results', {}), key_prefix=key_prefix)

        self._display_summary(summary=results.get('summary', {}))

    def _create_performance_charts(self: Self, results: Dict[str, Any], key_prefix: str = "") -> None:

        try:
            frameworks = list(results.keys())
            serialization_times = [results[fw]['avg_serialization_time']*1000 for fw in frameworks]  # ms
            deserialization_times = [results[fw]['avg_deserialization_time']*1000 for fw in frameworks]  # ms
            memory_usages = [results[fw]['avg_memory_usage']/1024 for fw in frameworks]  # KB

            col1, col2= st.columns(2)

            with col1:
                fig_ser = px.bar(
                    x=frameworks,
                    y=serialization_times,
                    color=serialization_times,
                    color_continuous_scale='RdYlBu_r',
                    title='Average Serialization Time by Framework',
                    labels={'x': 'Framework', 'y': 'Avg Serialization Time (ms)'},
                )
                fig_ser.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_ser, use_container_width=True, key=f"{key_prefix}serialization_chart")

            with col2:
                fig_deser = px.bar(
                    x=frameworks,
                    y=deserialization_times,
                    color=deserialization_times,
                    color_continuous_scale='RdYlBu_r',
                    title='Average Deserialization Time by Framework',
                    labels={'x': 'Framework', 'y': 'Avg Deserialization Time (ms)'},
                )
                fig_deser.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_deser, use_container_width=True, key=f"{key_prefix}deserialization_chart")

            fig_mem = px.bar(
                x=frameworks,
                y=memory_usages,
                color=memory_usages,
                color_continuous_scale='RdYlBu_r',
                title='Average Memory Usage by Framework',
                labels={'x': 'Framework', 'y': 'Avg Memory Usage (KB)'},
            )
            fig_mem.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_mem, use_container_width=True, key=f"{key_prefix}memory_chart")

            self._create_radar_chart(
                frameworks=frameworks,
                memory_usages=memory_usages,
                serialization_times=serialization_times,
                deserialization_times=deserialization_times,
                key_prefix=key_prefix,
            )

        except Exception as e:
            st.error(f"Error creating charts: {str(e)}")
            st.subheader("Performance Metrics")
            for fw, data in results.items():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"{fw} - Serialization (ms)", f"{data['avg_serialization_time']*1000:.3f}")
                with col2:
                    st.metric(f"{fw} - Deserialization (ms)", f"{data['avg_deserialization_time']*1000:.3f}")
                with col3:
                    st.metric(f"{fw} - Memory (KB)", f"{data['avg_memory_usage']/1024:.1f}")

    def _create_radar_chart(
        self: Self,
        frameworks: List[str],
        serialization_times: List[float],
        deserialization_times: List[float],
        memory_usages: List[float],
        key_prefix: str = "",
    ) -> None:
        
        try:
            # Normalize data for radar chart:
            max_ser = max(serialization_times) if serialization_times else 1
            max_deser = max(deserialization_times) if deserialization_times else 1
            max_mem = max(memory_usages) if memory_usages else 1

            fig = go.Figure()

            for i, framework in enumerate(frameworks):
                fig.add_trace(go.Scatterpolar(
                    r=[
                        (max_ser - serialization_times[i]) / max_ser * 100,
                        (max_deser - deserialization_times[i]) / max_deser * 100,
                        (max_mem - memory_usages[i]) / max_mem * 100 if memory_usages[i] > 0 else 100,
                    ],
                    theta=['Serialization Time', 'Deserialization Time', 'Memory Usage'],
                    fill='toself',
                    name=framework.title(),
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True, 
                        range=[0, 100],
                    )
                ),
                height=400,
                showlegend=True,
                title="🎯 Overall Framework Performance Comparison (Higher is Better)",
            )
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}radar_chart")

        except Exception as e:
            st.warning(f"Could not create radar chart: {str(e)}")

    def _display_summary(
        self: Self,
        summary: Dict[str, str]
    ) -> None:
        
        if not summary:
            return
        
        st.subheader("🏆 Performance Winners")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="🚀 Fastest Instantiation",
                value=summary.get('fastest_instantiation', 'N/A').title(),
                help="Framework with the fastest serialization time"
            )
        with col2:
            st.metric(
                label="⚡ Fastest Serialization",
                value=summary.get('fastest_serialization', 'N/A').title(),
                help="Framework with the fastest deserialization time"
            )

        with col3:
            st.metric(
                label="⚡ Fastest Deserialization",
                value=summary.get('fastest_deserialization', 'N/A').title()
            )
        with col4:
            st.metric(
                label="💾 Lowest Memory Usage",
                value=summary.get('lowest_memory_usage', 'N/A').title(),
                help="Framework with the lowest memory usage",
            )


