import streamlit as st


st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide"
)

import ui
ui.inject_custom_css()
ui.top_navbar("About")

st.title("ℹ️ About Project")

st.subheader("Insurance Fraud Detection System")

st.write("""
This project is designed to predict whether an insurance claim
is fraudulent or not using Machine Learning.
""")


st.divider()


st.subheader("🤖 Machine Learning Algorithm")

st.write("""
The project uses **Logistic Regression**.

Logistic Regression is a supervised machine learning algorithm
commonly used for binary classification problems.
""")


st.subheader("🎯 Prediction")

st.write("""
The model predicts two possible outcomes:

- **0 → No Fraud**
- **1 → Fraud**
""")


st.divider()


st.subheader("📌 Input Features")

features = [
    "Age of Driver",
    "Safety Rating",
    "Annual Income",
    "Past Number of Claims",
    "Vehicle Price",
    "Total Claim"
]

for feature in features:
    st.write(f"• {feature}")


st.divider()


st.subheader("⚙️ Technology Used")

technologies = [
    "Python",
    "Pandas",
    "Scikit-learn",
    "Streamlit",
    "Logistic Regression"
]

for technology in technologies:
    st.write(f"• {technology}")


st.divider()


st.success(
    "🚗 This system helps identify potentially fraudulent "
    "insurance claims using machine learning."
)