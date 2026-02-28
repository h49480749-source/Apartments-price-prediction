from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI(title="Apartments Price Prediction API", version="1.0")
model = joblib.load("models/model.pkl")

class ApartmentFeatures(BaseModel):
    Area: int
    PrivateGarden: str
    Bedrooms: int
    Bathrooms: int
    Payment : str
    Ownership : str
    Status : str



@app.post("/predict")
def predict(data: ApartmentFeatures):

    PrivateGarden = 1 if data.PrivateGarden == 'Yes' else 0
    total_rooms = data.Bedrooms + data.Bathrooms
    Payment_Cash_or_Installment = 1 if data.Payment == "Cash or Installment" else 0
    Payment_Installment = 1 if data.Payment == "Installment" else 0
    Ownership_Primary = 1 if data.Ownership == "Primary" else 0
    Status_Off_plan = 1 if data.Status == "Off-plan" else 0

    features = np.array([[data.Area, PrivateGarden, total_rooms,
                          Payment_Cash_or_Installment, Payment_Installment, Ownership_Primary, Status_Off_plan]])
    prediction = model.predict(features)

    return {"predicted_price": float(prediction[0])}