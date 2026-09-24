import streamlit as st
import pandas as pd
import sys
import os

# Add backend directory to path so we can import models and database
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from database import SessionLocal
import models
import ui

st.set_page_config(
    page_title="Case Management",
    page_icon="💼",
    layout="wide"
)

ui.inject_custom_css()
ui.top_navbar("Cases")

st.title("💼 Case Management Queue")
st.markdown("Review and investigate flagged claims detected by the ML engine.")

def get_logs():
    db = SessionLocal()
    try:
        logs = db.query(models.PredictionLog).order_by(models.PredictionLog.timestamp.desc()).all()
        
        if not logs:
            return pd.DataFrame()
        
        # Convert to dictionary and then to pandas DataFrame
        data = []
        for log in logs:
            data.append({
                "ID": log.id,
                "Timestamp": log.timestamp,
                "Prediction": log.result_text,
                "Fraud Prob (%)": log.fraud_probability,
                "Total Claim": log.total_claim,
                "Driver Age": log.age_of_driver,
                "Status": "Pending Review" if log.result_text == "Fraud" else "Auto-Approved"
            })
        return pd.DataFrame(data)
    finally:
        db.close()

df_logs = get_logs()

if df_logs.empty:
    st.info("No predictions logged yet. Go to 'Fraud Prediction' to make some API requests.")
else:
    st.subheader("Recent Investigations Queue")
    
    # Filter for active cases
    pending_cases = df_logs[df_logs["Status"] == "Pending Review"]
    
    if not pending_cases.empty:
        st.warning(f"⚠️ Action Required: {len(pending_cases)} claims flagged for human review.")
    else:
        st.success("✅ All clear. No pending reviews.")
    
    st.dataframe(df_logs, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("Case Actions")
    case_id = st.text_input("Enter Case ID to investigate:")
    if st.button("Open Case", type="primary"):
        if case_id:
            st.info(f"Opening detailed investigation view for Case ID: {case_id}... (Simulation)")
        else:
            st.error("Please enter a valid Case ID.")
