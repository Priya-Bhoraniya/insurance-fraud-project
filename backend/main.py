from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
from . import models
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.preprocessing import StandardScaler

from fastapi.middleware.cors import CORSMiddleware


# ==========================================
# FastAPI App
# ==========================================

app = FastAPI(
    title="Insurance Fraud Detection API",
    description="FastAPI backend for Insurance Fraud Detection",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
# Load Dataset
# ==========================================
df = pd.read_csv("insurance_fraud_data.csv")

for f in features:
    df[f] = pd.to_numeric(df[f], errors='coerce')

df = df.dropna(subset=features + ["fraud reported"])


# ==========================================
# Prepare Data
# ==========================================

X = df[features]

Y = df["fraud reported"].map({
    "N": 0,
    "Y": 1
})

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
# Train Logistic Regression
# ==========================================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train_scaled, Y_train)


# ==========================================
# Test Prediction
# ==========================================

Y_pred = model.predict(X_test_scaled)

Y_probability = model.predict_proba(X_test_scaled)


# ==========================================
# Evaluation Metrics
# ==========================================

accuracy = accuracy_score(Y_test, Y_pred)

precision = precision_score(
    Y_test,
    Y_pred,
    zero_division=0
)

recall = recall_score(
    Y_test,
    Y_pred,
    zero_division=0
)

f1 = f1_score(
    Y_test,
    Y_pred,
    zero_division=0
)

cm = confusion_matrix(
    Y_test,
    Y_pred
)


# ==========================================
# Request Schema
# ==========================================

class InsuranceData(BaseModel):

    age_of_driver: float
    marital_status: float
    safety_rating: float
    annual_income: float
    high_education: float
    address_change: float
    past_num_of_claims: float
    witness_present: float
    liab_prct: float
    police_report: float
    age_of_vehicle: float
    vehicle_price: float
    total_claim: float
    injury_claim: float
    policy_deductible: float
    annual_premium: float
    days_open: float
    form_defects: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "age_of_driver": 30.0,
                    "marital_status": 1.0,
                    "safety_rating": 3.0,
                    "annual_income": 50000.0,
                    "high_education": 1.0,
                    "address_change": 0.0,
                    "past_num_of_claims": 1.0,
                    "witness_present": 0.0,
                    "liab_prct": 25.0,
                    "police_report": 0.0,
                    "age_of_vehicle": 5.0,
                    "vehicle_price": 25000.0,
                    "total_claim": 10000.0,
                    "injury_claim": 2000.0,
                    "policy_deductible": 500.0,
                    "annual_premium": 1200.0,
                    "days_open": 10.0,
                    "form_defects": 2.0
                }
            ]
        }
    }


# ==========================================
# Home API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Insurance Fraud Detection API is running",
        "model": "Logistic Regression"
    }


# ==========================================
# Prediction API
# ==========================================

@app.post("/predict")
def predict(data: InsuranceData, db: Session = Depends(get_db)):

    input_data = pd.DataFrame(
        [[
            data.age_of_driver,
            data.marital_status,
            data.safety_rating,
            data.annual_income,
            data.high_education,
            data.address_change,
            data.past_num_of_claims,
            data.witness_present,
            data.liab_prct,
            data.police_report,
            data.age_of_vehicle,
            data.vehicle_price,
            data.total_claim,
            data.injury_claim,
            data.policy_deductible,
            data.annual_premium,
            data.days_open,
            data.form_defects
        ]],
        columns=features
    )

    input_data_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data_scaled)

    probability = model.predict_proba(input_data_scaled)

    fraud_probability = probability[0][1] * 100

    if prediction[0] == 1:

        result = "Fraud"

    else:

        result = "No Fraud"
        
    # Log prediction to database
    db_log = models.PredictionLog(
        age_of_driver=data.age_of_driver,
        marital_status=data.marital_status,
        safety_rating=data.safety_rating,
        annual_income=data.annual_income,
        high_education=data.high_education,
        address_change=data.address_change,
        past_num_of_claims=data.past_num_of_claims,
        witness_present=data.witness_present,
        liab_prct=data.liab_prct,
        police_report=data.police_report,
        age_of_vehicle=data.age_of_vehicle,
        vehicle_price=data.vehicle_price,
        total_claim=data.total_claim,
        injury_claim=data.injury_claim,
        policy_deductible=data.policy_deductible,
        annual_premium=data.annual_premium,
        days_open=data.days_open,
        form_defects=data.form_defects,
        prediction=int(prediction[0]),
        result_text=result,
        fraud_probability=round(fraud_probability, 2)
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return {
        "prediction": int(prediction[0]),
        "result": result,
        "fraud_probability": round(
            fraud_probability,
            2
        ),
        "log_id": db_log.id
    }


# ==========================================
# Model Evaluation API
# ==========================================

@app.get("/model/evaluation")
def model_evaluation():

    return {

        "model": "Logistic Regression",

        "training_samples": len(X_train),

        "testing_samples": len(X_test),

        "accuracy": round(
            accuracy,
            4
        ),

        "accuracy_percentage": round(
            accuracy * 100,
            2
        ),

        "precision": round(
            precision,
            4
        ),

        "recall": round(
            recall,
            4
        ),

        "f1_score": round(
            f1,
            4
        )
    }


# ==========================================
# Confusion Matrix API
# ==========================================

@app.get("/model/confusion-matrix")
def get_confusion_matrix():

    return {

        "labels": [
            "No Fraud",
            "Fraud"
        ],

        "matrix": cm.tolist(),

        "true_negative": int(cm[0][0]),

        "false_positive": int(cm[0][1]),

        "false_negative": int(cm[1][0]),

        "true_positive": int(cm[1][1])
    }


# ==========================================
# Classification Report API
# ==========================================

@app.get("/model/classification-report")
def classification_report_api():

    report = classification_report(
        Y_test,
        Y_pred,
        target_names=[
            "No Fraud",
            "Fraud"
        ],
        output_dict=True
    )

    return report


# ==========================================
# Model Information API
# ==========================================

@app.get("/model/info")
def model_info():

    return {

        "algorithm": "Logistic Regression",

        "problem_type": "Binary Classification",

        "target": "fraud reported",

        "target_mapping": {
            "0": "No Fraud",
            "1": "Fraud"
        },

        "features": features,

        "training_samples": len(X_train),

        "testing_samples": len(X_test)
    }