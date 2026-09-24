import streamlit as st
import pandas as pd

from backend.database import SessionLocal
from backend import models

import ui


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Case Management",
    page_icon="💼",
    layout="wide"
)


# ==========================================
# UI
# ==========================================

ui.inject_custom_css()
ui.top_navbar("Cases")

st.title("💼 Case Management Queue")

st.markdown(
    "Review and investigate flagged claims detected by the ML engine."
)


# ==========================================
# Get Prediction Logs
# ==========================================

def get_logs():

    db = SessionLocal()

    try:

        logs = (
            db.query(models.PredictionLog)
            .order_by(
                models.PredictionLog.timestamp.desc()
            )
            .all()
        )

        if not logs:
            return pd.DataFrame()

        data = []

        for log in logs:

            data.append({
                "ID": log.id,
                "Timestamp": log.timestamp,
                "Prediction": log.result_text,
                "Fraud Prob (%)": log.fraud_probability,
                "Total Claim": log.total_claim,
                "Driver Age": log.age_of_driver,
                "Status": (
                    "Pending Review"
                    if log.result_text == "Fraud"
                    else "Auto-Approved"
                )
            })

        return pd.DataFrame(data)

    finally:
        db.close()


# ==========================================
# Load Logs
# ==========================================

try:

    df_logs = get_logs()

except Exception as e:

    st.error(
        f"Unable to load case data: {e}"
    )

    df_logs = pd.DataFrame()


# ==========================================
# Display Cases
# ==========================================

if df_logs.empty:

    st.info(
        "No predictions logged yet. "
        "Go to 'Fraud Prediction' to make some API requests."
    )

else:

    st.subheader("Recent Investigations Queue")

    # ======================================
    # Pending Cases
    # ======================================

    pending_cases = df_logs[
        df_logs["Status"] == "Pending Review"
    ]

    if not pending_cases.empty:

        st.warning(
            f"⚠️ Action Required: "
            f"{len(pending_cases)} claims flagged for human review."
        )

    else:

        st.success(
            "✅ All clear. No pending reviews."
        )


    # ======================================
    # Case Table
    # ======================================

    st.dataframe(
        df_logs,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ======================================
    # Case Actions
    # ======================================

    st.subheader("Case Actions")

    case_id = st.text_input(
        "Enter Case ID to investigate:"
    )

    if st.button(
        "Open Case",
        type="primary"
    ):

        if case_id:

            st.info(
                f"Opening detailed investigation view "
                f"for Case ID: {case_id}... (Simulation)"
            )

        else:

            st.error(
                "Please enter a valid Case ID."
            )