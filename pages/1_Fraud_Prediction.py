# http://localhost:8501/

import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Fraud Prediction",
    page_icon="🔍",
    layout="wide"
)

import ui
ui.inject_custom_css()
ui.top_navbar("Prediction")

# Display the stunning vehicle fraud banner
st.image("assets/ins_fraud_banner_1788292068124.jpg", use_container_width=True)

# ==========================================
# Load Dataset
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv("insurance_fraud_data.csv")


df = load_data()


# ==========================================
# Features
# ==========================================

features = [
    "age_of_driver",
    "marital_status",
    "safety_rating",
    "annual_income",
    "high_education",
    "address_change",
    "past_num_of_claims",
    "witness_present",
    "liab_prct",
    "police_report",
    "age_of_vehicle",
    "vehicle_price",
    "total_claim",
    "injury_claim",
    "policy deductible",
    "annual premium",
    "days open",
    "form defects"
]


# ==========================================
# Remove Missing Target Values
# ==========================================

for f in features:
    df[f] = pd.to_numeric(df[f], errors='coerce')

df = df.dropna(subset=features + ["fraud reported"])


X = df[features]


# ==========================================
# Target
# ==========================================

Y = df["fraud reported"].map({
    "N": 0,
    "Y": 1
})


# Remove rows where target mapping failed
valid_rows = Y.notna()

X = X[valid_rows]
Y = Y[valid_rows]


# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# Logistic Regression
# ==========================================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)

model.fit(X_train_scaled, Y_train)


# ==========================================
# Accuracy
# ==========================================

Y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(Y_test, Y_pred)


# ==========================================
# Page Header
# ==========================================

st.title("🔍 Insurance Fraud Prediction")

st.write(
    "Enter the insurance claim details below to predict "
    "whether the claim is fraudulent or not."
)

st.divider()


# ==========================================
# Input Section
# ==========================================

st.subheader("📝 Enter Insurance Details")

col1, col2 = st.columns(2)


with col1:

    age_of_driver = st.number_input("Age of Driver", min_value=18, max_value=100, value=30, step=1)
    safety_rating = st.number_input("Safety Rating", min_value=1, max_value=100, value=75, step=1)
    annual_income = st.number_input("Annual Income", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
    high_education = st.number_input("High Education (0 or 1)", min_value=0, max_value=1, value=1, step=1)
    past_num_of_claims = st.number_input("Past Number of Claims", min_value=0, value=1, step=1)
    liab_prct = st.number_input("Liability Percentage", min_value=0, max_value=100, value=25, step=1)
    age_of_vehicle = st.number_input("Age of Vehicle", min_value=0.0, value=5.0, step=1.0)
    total_claim = st.number_input("Total Claim", min_value=0.0, value=10000.0, step=1000.0, format="%.2f")
    policy_deductible = st.number_input("Policy Deductible", min_value=0.0, value=500.0, step=100.0)

with col2:

    marital_status = st.number_input("Marital Status (0 or 1)", min_value=0, max_value=1, value=1, step=1)
    address_change = st.number_input("Address Change (0 or 1)", min_value=0, max_value=1, value=0, step=1)
    witness_present = st.number_input("Witness Present (0 or 1)", min_value=0, max_value=1, value=0, step=1)
    police_report = st.number_input("Police Report (0 or 1)", min_value=0, max_value=1, value=0, step=1)
    vehicle_price = st.number_input("Vehicle Price", min_value=0.0, value=25000.0, step=1000.0, format="%.2f")
    injury_claim = st.number_input("Injury Claim", min_value=0.0, value=2000.0, step=1000.0, format="%.2f")
    annual_premium = st.number_input("Annual Premium", min_value=0.0, value=1200.0, step=100.0)
    days_open = st.number_input("Days Open", min_value=0.0, value=10.0, step=1.0)
    form_defects = st.number_input("Form Defects", min_value=0, value=0, step=1)



st.divider()


# ==========================================
# Prediction Button
# ==========================================

if st.button(
    "🔍 Predict Fraud",
    use_container_width=True,
    type="primary"
):

    input_data = pd.DataFrame(
        [[
            age_of_driver,
            marital_status,
            safety_rating,
            annual_income,
            high_education,
            address_change,
            past_num_of_claims,
            witness_present,
            liab_prct,
            police_report,
            age_of_vehicle,
            vehicle_price,
            total_claim,
            injury_claim,
            policy_deductible,
            annual_premium,
            days_open,
            form_defects
        ]],
        columns=features
    )


    # Prediction
    input_data_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data_scaled)


    # Probability
    probability = model.predict_proba(input_data_scaled)

    fraud_probability = probability[0][1] * 100


    # ======================================
    # Result
    # ======================================

    st.subheader("📋 Prediction Result")


    if prediction[0] == 1:

        st.error(
            "🔴 Fraud Reported: YES"
        )

        st.warning(
            f"⚠️ Fraud Probability: {fraud_probability:.2f}%"
        )

    else:

        st.success(
            "🟢 Fraud Reported: NO"
        )

        st.info(
            f"Fraud Probability: {fraud_probability:.2f}%"
        )

    # Save to Backend via API
    import requests
    try:
        payload = {
            "age_of_driver": int(age_of_driver),
            "marital_status": int(marital_status),
            "safety_rating": int(safety_rating),
            "annual_income": float(annual_income),
            "high_education": int(high_education),
            "address_change": int(address_change),
            "past_num_of_claims": int(past_num_of_claims),
            "witness_present": int(witness_present),
            "liab_prct": int(liab_prct),
            "police_report": int(police_report),
            "age_of_vehicle": float(age_of_vehicle),
            "vehicle_price": float(vehicle_price),
            "total_claim": float(total_claim),
            "injury_claim": float(injury_claim),
            "policy_deductible": float(policy_deductible),
            "annual_premium": float(annual_premium),
            "days_open": float(days_open),
            "form_defects": int(form_defects)
        }
        requests.post("http://localhost:8000/predict", json=payload)
    except Exception as e:
        st.caption("Note: Prediction was not saved to Case Management queue because backend is offline.")


    # Probability bar and Gauge Chart
    import plotly.graph_objects as go
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = fraud_probability,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score", 'font': {'size': 24, 'color': 'white'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#f5576c" if prediction[0] == 1 else "#00f2fe"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(0, 242, 254, 0.2)'},
                {'range': [30, 70], 'color': 'rgba(240, 147, 251, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(245, 87, 108, 0.2)'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50}
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Outfit"},
        margin=dict(t=50, b=0, l=0, r=0),
        height=300
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)


# ==========================================
# Model Accuracy
# ==========================================

st.divider()

st.subheader("📊 Model Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Model Accuracy",
        f"{accuracy * 100:.2f}%"
    )

with col2:
    st.metric(
        "Training Records",
        len(X_train)
    )

with col3:
    st.metric(
        "Testing Records",
        len(X_test)
    )
    
    #http://localhost:8501/
    #http://localhost:8501/Fraud_Prediction