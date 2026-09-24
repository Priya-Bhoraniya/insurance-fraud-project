import streamlit as st
import time
import psutil
import requests
import ui
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="System Health & MLOps",
    page_icon="⚙️",
    layout="wide"
)

ui.inject_custom_css()
ui.top_navbar("Health")

st.title("⚙️ System Health & MLOps")
st.markdown("Real-time monitoring of backend APIs, Database, and Model Drift.")

st.divider()

col1, col2, col3 = st.columns(3)

# 1. API Health
with col1:
    st.subheader("API Status")
    try:
        # Check backend running
        start_time = time.time()
        res = requests.get("http://localhost:8000/")
        latency = (time.time() - start_time) * 1000
        if res.status_code == 200:
            st.success("🟢 Online (Connected)")
            st.metric("Latency", f"{latency:.2f} ms")
        else:
            st.warning("🟡 Degraded")
    except Exception:
        st.error("🔴 Offline (Backend Unreachable)")
        st.caption("Ensure `uvicorn backend.main:app` is running.")

# 2. Server Metrics (Simulated or Real)
with col2:
    st.subheader("Server Resources")
    cpu_usage = psutil.cpu_percent(interval=0.1)
    mem_usage = psutil.virtual_memory().percent
    
    st.metric("CPU Load", f"{cpu_usage}%")
    st.metric("Memory Usage", f"{mem_usage}%")
    
# 3. Model Versioning
with col3:
    st.subheader("Model Registry")
    st.metric("Active Model", "Logistic Regression v1.2")
    st.metric("Features", "18 Normalized Inputs")
    st.metric("Last Retrained", "Today, 02:00 AM")

st.divider()

# Model Drift Simulation
st.subheader("Data Drift Detection (Simulated)")
st.markdown("Monitoring input features over time to detect shifts in distribution that could impact model performance.")

# Mock drift data
dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
drift_scores = np.random.normal(loc=0.05, scale=0.02, size=30)
drift_scores[-5:] = drift_scores[-5:] + np.random.uniform(0.05, 0.15, size=5) # Simulate recent drift

drift_df = pd.DataFrame({
    "Date": dates,
    "Feature Drift Score (KL Divergence)": drift_scores
})

fig = px.line(
    drift_df, 
    x="Date", 
    y="Feature Drift Score (KL Divergence)", 
    title="Data Drift over last 30 days"
)

# Add alert line
fig.add_hline(y=0.15, line_dash="dash", line_color="red", annotation_text="Drift Alert Threshold")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")

st.plotly_chart(fig, use_container_width=True)

if drift_scores[-1] > 0.15:
    st.error("⚠️ ALERT: High Data Drift Detected. Model retraining is highly recommended.")
else:
    st.success("✅ Data distributions are stable. No immediate retraining required.")
