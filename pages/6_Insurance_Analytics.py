import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ui

st.set_page_config(
    page_title="Insurance Analytics",
    page_icon="📈",
    layout="wide"
)

ui.inject_custom_css()
ui.top_navbar("Analytics")

# Display the stunning vehicle analytics banner
st.image("assets/ins_analytics_banner_1788292078459.jpg", use_container_width=True)
st.title("📈 Advanced Vehicle Telemetry & Analytics")
st.markdown("Explore deep insights, telemetry, and fraud distribution across the insurance dataset using modern interactive visualizations.")

@st.cache_data
def load_data():
    return pd.read_csv("insurance_fraud_data.csv")

try:
    df = load_data()
    
    # Custom color sequence for the neon theme
    neon_colors = ['#00f2fe', '#f093fb', '#f5576c', '#4facfe', '#00ff87']
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Fraud Hierarchy Analysis")
        st.markdown("A deep dive into how fraud distribution correlates with the accident site and vehicle category.")
        # Creative Sunburst Chart
        fig_sunburst = px.sunburst(
            df, 
            path=['fraud reported', 'accident_site', 'vehicle_category'], 
            values='total_claim',
            color='fraud reported',
            color_discrete_map={'Y': '#f5576c', 'N': '#00f2fe'},
            template='plotly_dark'
        )
        fig_sunburst.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)

    with col2:
        st.subheader("🧊 3D Telemetry Correlation")
        st.markdown("Interactive 3D mapping of Driver Age, Vehicle Price, and Total Claim Amount.")
        # Creative 3D Scatter
        fig_3d = px.scatter_3d(
            df, 
            x='age_of_driver', 
            y='vehicle_price', 
            z='total_claim',
            color='fraud reported',
            size_max=18,
            opacity=0.8,
            color_discrete_map={'Y': '#f5576c', 'N': '#00f2fe'},
            template='plotly_dark'
        )
        fig_3d.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
            )
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🎼 Claim Distribution Density")
        st.markdown("Violin plot showing the density and distribution of claims by Marital Status.")
        fig_violin = px.violin(
            df, 
            y="total_claim", 
            x="marital_status", 
            color="fraud reported", 
            box=True, 
            points="all",
            color_discrete_map={'Y': '#f5576c', 'N': '#00f2fe'},
            template='plotly_dark'
        )
        fig_violin.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
    with col4:
        st.subheader("🔥 Claim Frequency Heatmap")
        st.markdown("Density heatmap of Police Reports vs Education Level.")
        fig_heatmap = px.density_heatmap(
            df, 
            x="high_education", 
            y="police_report", 
            z="total_claim",
            histfunc="avg",
            color_continuous_scale="Purp",
            template='plotly_dark'
        )
        fig_heatmap.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data for analytics: {e}")
