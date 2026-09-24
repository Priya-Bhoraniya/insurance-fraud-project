
# http://localhost:8501/
import streamlit as st
import ui

st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="🚗",
    layout="wide"
)

ui.inject_custom_css()
ui.top_navbar("Home")

# Display the stunning vehicle hero banner
st.image("/Users/priyabhoraniya/.gemini/antigravity-ide/brain/53372486-ca7f-435b-9a27-0f443dc16077/ins_hero_banner_1788292056689.jpg", use_container_width=True)

st.title("🚗 Insurance Fraud Detection System")

st.markdown("""
## Welcome to the Future of Risk Analysis!

Vehicle insurance fraud costs the global industry billions of dollars annually, driving up premiums for honest drivers and causing massive inefficiencies in claim processing. 

This cutting-edge **Vehicle Insurance Fraud Detection System** leverages state-of-the-art **Machine Learning (Logistic Regression)** to instantly analyze claim telemetry, driver demographics, and vehicle details to predict the likelihood of a fraudulent claim.

### 🌟 Project Highlights
- **Automated Risk Scoring:** Instantly evaluate the authenticity of an insurance claim using high-dimensional data points.
- **Deep Telemetry Analytics:** Explore the interactive analytics dashboard to visualize the correlation between vehicle price, accident severity, and fraud density.
- **Real-Time Prediction:** Input claim metrics and receive a live probability score.

### 🧭 Available Workspaces

Use the frosted glass sidebar on the left to navigate the system:

- 📈 **Executive Dashboard:** High-level metrics on fraud rates, case volumes, and savings.
- 🔍 **Fraud Prediction:** Real-time form to input new claims and evaluate their fraud probability.
- 💼 **Case Management:** Review queue for flagged claims requiring human investigation.
- ⚙️ **System Health:** Monitor real-time API latency, backend resources, and model data drift.
- 📊 **Model Performance:** Detailed AI accuracy metrics, confusion matrices, and precision/recall scores.
- 🧠 **Model Designer:** A powerful studio where you can train custom machine learning architectures (Decision Trees, Random Forests) live in your browser.
- 📈 **Insurance Analytics:** Highly interactive 3D and hierarchical visualizations of the insurance dataset.
- ℹ️ **About Project:** Details regarding the methodology and data.
- 📞 **Contact:** Developer information.

### ⚙️ How the Prediction Engine Works

1. Enter detailed insurance claim metrics (e.g., Vehicle Price, Driver Age, Liability, Annual Premium).
2. Click the **Predict Fraud** button to send data to the backend AI.
3. The trained ML model processes the inputs against historical fraud patterns.
4. The system instantly returns a high-precision binary decision (Fraud / No Fraud) alongside a detailed probability risk score.
5. High-risk claims are automatically routed to the **Case Management** queue for human investigation.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model", "Logistic Regression")

with col2:
    st.metric("Prediction Type", "Binary Classification")

with col3:
    st.metric("Target", "Fraud / No Fraud")

st.info("👈 Select a page from the sidebar to continue.")