from fastapi import FastAPI, HTTPException
from .schemas import Transaction
from .model import FraudDetector
import torch
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Real-time fraud prediction system",
    version="1.0.0"
)

# Load model
MODEL_PATH = os.getenv("MODEL_PATH", "../models/credit_card_fraud_model.pth")

try:
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    FEATURE_COLS = checkpoint['feature_cols']
    input_size = checkpoint['input_size']
    scaler = checkpoint['scaler']
    
    model = FraudDetector(input_size)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Model loading failed: {str(e)}")
    raise RuntimeError("Model initialization failed")

@app.post("/predict", summary="Predict fraud probability")
async def predict(transaction: Transaction):
    try:
        # Convert to DataFrame
        data = transaction.dict()
        df = pd.DataFrame([data])
        
        # Feature engineering
        df['hour'] = df['Time'] % (24*60*60) // (60*60)
        df['amount_log'] = np.log1p(df['Amount'])
        
        # Select and scale features
        features = df[FEATURE_COLS].values
        scaled = scaler.transform(features)
        features_tensor = torch.tensor(scaled, dtype=torch.float)
        
        # Predict
        with torch.no_grad():
            prob = model(features_tensor)
        
        return {
            "fraud_probability": float(prob.item()),
            "risk_level": "high" if prob > 0.7 else "medium" if prob > 0.3 else "low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {
        "status": "active",
        "model": "CreditCardFraudDetector",
        "version": "1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)