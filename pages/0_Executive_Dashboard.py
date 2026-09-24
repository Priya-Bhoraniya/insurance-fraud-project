import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ui

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📈",
    layout="wide"
)

ui.inject_custom_css()
ui.top_navbar("Dashboard")

st.title("📈 Executive Dashboard")
st.markdown("Real-time high-level metrics of the Fraud Management System.")

@st.cache_data
def load_data():
    df = pd.read_csv("insurance_fraud_data.csv")
    df = df.dropna(subset=["fraud reported"])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading historical data: {e}")
    st.stop()

st.divider()

# Top Metrics
st.subheader("Key Performance Indicators")

total_claims = len(df)
fraud_claims = len(df[df["fraud reported"] == "Y"])
fraud_percentage = (fraud_claims / total_claims) * 100
total_fraud_value = df[df["fraud reported"] == "Y"]["total_claim"].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Claims Analyzed", f"{total_claims:,}")
with col2:
    st.metric("Fraud Cases Detected", f"{fraud_claims:,}")
with col3:
    st.metric("Fraud Rate", f"{fraud_percentage:.2f}%")
with col4:
    st.metric("Potential Savings", f"${total_fraud_value:,.2f}")

st.divider()

# Charts
st.subheader("Fraud Distribution Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Fraud by vehicle category
    fraud_by_category = df[df["fraud reported"] == "Y"].groupby("vehicle_category").size().reset_index(name='count')
    fig1 = px.pie(
        fraud_by_category, 
        values='count', 
        names='vehicle_category', 
        title="Fraud Detected by Vehicle Category",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    # Average total claim by fraud status
    claim_by_fraud = df.groupby("fraud reported")["total_claim"].mean().reset_index()
    fig2 = px.bar(
        claim_by_fraud, 
        x="fraud reported", 
        y="total_claim", 
        title="Average Total Claim Value ($)",
        color="fraud reported",
        color_discrete_sequence=["#00f2fe", "#f5576c"]
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Recent System Activity")
st.info("System is actively monitoring incoming claims. Navigate to the Case Management page to review pending investigations.")
