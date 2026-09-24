import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)


st.set_page_config(
    page_title="Model Performance",
    page_icon="📊",
    layout="wide"
)

import ui
ui.inject_custom_css()
ui.top_navbar("Performance")

# Display the stunning vehicle performance banner
st.image("assets/ins_analytics_banner_1788292078459.jpg", use_container_width=True)
st.title("📊 Model Performance")

st.write(
    "This page shows the performance of the Logistic Regression "
    "model used for insurance fraud prediction."
)


# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("insurance_fraud_data.csv")

df = df.dropna(subset=["fraud reported"])


features = [
    "age_of_driver",
    "safety_rating",
    "annual_income",
    "past_num_of_claims",
    "vehicle_price",
    "total_claim"
]


X = df[features]

Y = df["fraud reported"].map({
    "N": 0,
    "Y": 1
})

valid_rows = Y.notna()

X = X[valid_rows]
Y = Y[valid_rows]


# ==========================================
# Train Test
# ==========================================

X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# Model
# ==========================================

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)


# ==========================================
# Metrics
# ==========================================

accuracy = accuracy_score(
    Y_test,
    Y_pred
)

cm = confusion_matrix(
    Y_test,
    Y_pred
)


# ==========================================
# Metrics Display
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Accuracy",
        f"{accuracy * 100:.2f}%"
    )

with col2:
    st.metric(
        "Training Data",
        len(X_train)
    )

with col3:
    st.metric(
        "Testing Data",
        len(X_test)
    )


st.divider()


# ==========================================
# Feature Importance
# ==========================================

st.subheader("📌 Feature Importance (Coefficients)")
st.markdown("This bar chart visualizes the importance (weight) the AI assigns to each feature when predicting fraud.")

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=True)

fig_coef = px.bar(
    coef_df, 
    x='Coefficient', 
    y='Feature', 
    orientation='h',
    color='Coefficient',
    color_continuous_scale=['#00f2fe', '#f5576c'],
    template='plotly_dark'
)
fig_coef.update_layout(
    margin=dict(t=10, l=10, r=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_coef, use_container_width=True)

st.divider()

# ==========================================
# Confusion Matrix
# ==========================================

st.subheader("🔢 Confusion Matrix")
st.markdown("Visualizing True Positives, True Negatives, False Positives, and False Negatives.")

x = ['Predicted No Fraud', 'Predicted Fraud']
y = ['Actual No Fraud', 'Actual Fraud']
z = cm[::-1] # Reverse rows for proper heatmap orientation

fig_cm = ff.create_annotated_heatmap(
    z, x=x, y=y[::-1], 
    colorscale=['#00f2fe', '#130022', '#f5576c'], 
    showscale=True
)
fig_cm.update_layout(
    template='plotly_dark',
    margin=dict(t=40, l=10, r=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_cm, use_container_width=True)


st.divider()


# ==========================================
# Classification Report
# ==========================================

st.subheader("📈 Classification Report")
st.markdown("Visualizing Precision, Recall, and F1-Score.")

report = classification_report(
    Y_test,
    Y_pred,
    target_names=["No Fraud", "Fraud"],
    output_dict=True
)

# Extract main metrics
metrics_df = pd.DataFrame({
    'Class': ['No Fraud', 'Fraud'],
    'Precision': [report['No Fraud']['precision'], report['Fraud']['precision']],
    'Recall': [report['No Fraud']['recall'], report['Fraud']['recall']],
    'F1-Score': [report['No Fraud']['f1-score'], report['Fraud']['f1-score']]
})

# Melt for grouped bar chart
metrics_melted = metrics_df.melt(id_vars='Class', var_name='Metric', value_name='Score')

fig_metrics = px.bar(
    metrics_melted, 
    x='Class', 
    y='Score', 
    color='Metric', 
    barmode='group',
    color_discrete_sequence=['#00f2fe', '#f093fb', '#f5576c'],
    template='plotly_dark'
)
fig_metrics.update_layout(
    margin=dict(t=10, l=10, r=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(range=[0, 1])
)
st.plotly_chart(fig_metrics, use_container_width=True)