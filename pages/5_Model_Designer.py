import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
import ui

st.set_page_config(
    page_title="Model Designer Studio",
    page_icon="🧠",
    layout="wide"
)

ui.inject_custom_css()
ui.top_navbar("Designer")

# Display the stunning vehicle designer banner
st.image("assets/ins_designer_banner_1788292090868.jpg", use_container_width=True)
# Header
st.title("🧠 Model Designer Studio")
st.markdown("Configure and train custom models on the insurance dataset using this visual designer.")
st.divider()

# Layout
config_col, preview_col = st.columns([1, 2])

with config_col:
    st.subheader("1. Pipeline Config")
    
    available_features = [
        "age_of_driver", "marital_status", "safety_rating", "annual_income", 
        "high_education", "address_change", "past_num_of_claims", 
        "witness_present", "liab_prct", "police_report", "age_of_vehicle", 
        "vehicle_price", "total_claim", "injury_claim", 
        "policy deductible", "annual premium", "days open", "form defects"
    ]

    # Load dataset
    @st.cache_data
    def load_data():
        df = pd.read_csv("insurance_fraud_data.csv")
        for f in available_features:
            df[f] = pd.to_numeric(df[f], errors='coerce')
        df = df.dropna(subset=available_features + ["fraud reported"])
        return df

    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    selected_features = st.multiselect(
        "Select Features for Training",
        options=available_features,
        default=available_features
    )
    
    st.subheader("2. Architecture")
    
    model_type = st.selectbox(
        "Select Algorithm",
        options=["Logistic Regression", "Decision Tree", "Random Forest"]
    )
    
    st.subheader("3. Hyperparameters")
    
    if model_type == "Logistic Regression":
        max_iter = st.number_input("max_iter", min_value=100, max_value=5000, value=1000, step=100)
        c_val = st.number_input("C (Regularization)", min_value=0.01, max_value=10.0, value=1.0, step=0.1)
        model = LogisticRegression(max_iter=max_iter, C=c_val)
        
    elif model_type == "Decision Tree":
        max_depth = st.number_input("max_depth", min_value=1, max_value=50, value=5, step=1)
        min_samples_split = st.number_input("min_samples_split", min_value=2, max_value=20, value=2, step=1)
        model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, random_state=42)
        
    else: # Random Forest
        n_estimators = st.number_input("n_estimators", min_value=10, max_value=500, value=100, step=10)
        max_depth = st.number_input("max_depth", min_value=1, max_value=50, value=10, step=1)
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

with preview_col:
    st.subheader("Console Output")
    
    console = st.empty()
    console.info("> Awaiting configuration... Click 'Train Model' to begin.")
    
    train_button = st.button("🚀 Train Model", type="primary", use_container_width=True)
    
    if train_button:
        if len(selected_features) == 0:
            console.error("> Error: Please select at least one feature.")
        else:
            with st.spinner("Training model..."):
                # Prepare data
                X = df[selected_features]
                Y = df["fraud reported"].map({"N": 0, "Y": 1})
                
                valid_rows = Y.notna()
                X = X[valid_rows]
                Y = Y[valid_rows]
                
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
                
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                # Train
                model.fit(X_train_scaled, Y_train)
                Y_pred = model.predict(X_test_scaled)
                
                # Evaluate
                acc = accuracy_score(Y_test, Y_pred)
                prec = precision_score(Y_test, Y_pred, zero_division=0)
                rec = recall_score(Y_test, Y_pred, zero_division=0)
                
                console.success(f"> Model trained successfully using {model_type}.")
                
                st.divider()
                st.subheader("Performance Metrics")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Accuracy", f"{acc*100:.2f}%")
                m2.metric("Precision", f"{prec*100:.2f}%")
                m3.metric("Recall", f"{rec*100:.2f}%")
                
                st.divider()
                st.subheader("Pipeline Summary")
                st.json({
                    "Algorithm": model_type,
                    "Features Selected": selected_features,
                    "Training Samples": len(X_train),
                    "Test Samples": len(X_test),
                    "Hyperparameters": model.get_params()
                })
