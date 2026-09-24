from sqlalchemy import Column, Integer, Float, String, DateTime
from .database import Base
import datetime

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Input Features
    age_of_driver = Column(Float)
    marital_status = Column(Float)
    safety_rating = Column(Float)
    annual_income = Column(Float)
    high_education = Column(Float)
    address_change = Column(Float)
    past_num_of_claims = Column(Float)
    witness_present = Column(Float)
    liab_prct = Column(Float)
    police_report = Column(Float)
    age_of_vehicle = Column(Float)
    vehicle_price = Column(Float)
    total_claim = Column(Float)
    injury_claim = Column(Float)
    policy_deductible = Column(Float)
    annual_premium = Column(Float)
    days_open = Column(Float)
    form_defects = Column(Float)
    
    # Prediction Results
    prediction = Column(Integer)
    result_text = Column(String)
    fraud_probability = Column(Float)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
