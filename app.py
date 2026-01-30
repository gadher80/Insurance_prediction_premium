from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
from model.predict import predict_output, model_version, model
from schema.prediction_response import PredictionResponse
from schema.user_input import UserInput

app = FastAPI()

# Load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)


#add home route
@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API"}

@app.get("/health")
def health_check():

    return {"status": "OK", "model_version": model_version}




@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    input_df = {
        "bmi": [data.bmi],
        "age_group": [data.age_group],
        "lifestyle_risk": [data.lifestyle_risk],
        "city_tier": [data.city_tier],
        "income_lpa": [data.income_lpa],
        "occupation": [data.occupation]
    }
    try:
        prediction = predict_output(input_df)
        return JSONResponse(content={"predicted_premium": prediction})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
