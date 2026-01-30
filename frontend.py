import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Predictor")

age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
height = st.number_input("Height (cm)", min_value=50.0, value=175.0)
income_lpa = st.number_input("Income (LPA)", min_value=0.1, value=6.0)

smoker = st.selectbox("Smoker", ["Yes", "No"])

city = st.text_input("City", value="Mumbai")

occupation = st.selectbox(
    "Occupation",
    [
        "business_owner",
        "freelancer",
        "government_job",
        "private_job",
        "retired",
        "student",
        "unemployed"
    ]
)

if st.button("Predict Premium"):
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Premium: {result['predicted_premium']}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"Connection error: {e}")
