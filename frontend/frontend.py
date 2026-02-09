import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/predict"

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered"
)

# Light and minimal CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        max-width: 700px;
        margin: 0 auto;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 700px;
        margin: 0 auto;
        padding-right: 20px;
        padding-left: 20px;
    }
    .section-header {
        background-color: #e8eef5;
        padding: 12px;
        border-radius: 6px;
        margin: 20px 0 10px 0;
        font-size: 1.1rem;
        font-weight: 500;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ Insurance Premium Predictor")
st.markdown("**Predict your insurance premium with AI-powered insights**")
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("Select Section", ["Prediction", "Health Check"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    **Features Used:**
    - BMI (calculated from height & weight)
    - Age Group
    - Lifestyle Risk Assessment
    - City Tier
    - Annual Income
    - Occupation Type
    """)

if page == "Health Check":
    st.markdown('<div class="section-header">API Health Check</div>', unsafe_allow_html=True)
    
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Status: OK")
            with col2:
                st.info(f"Model Version: {health_data.get('model_version', 'Unknown')}")
        else:
            st.error("API is not responding")
    except Exception as e:
        st.error(f"Connection error: {e}")

else:
    # Personal Information Section
    st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=119, value=30)
    
    with col2:
        weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0, step=0.1)
    
    with col3:
        height = st.number_input("Height (cm)", min_value=50.0, value=175.0, step=0.1)
    
    # Health Metrics
    st.markdown('<div class="section-header">Health Metrics</div>', unsafe_allow_html=True)
    
    bmi = round(weight / ((height / 100) ** 2), 2)
    bmi_category = "Normal" if 18.5 <= bmi < 25 else ("Underweight" if bmi < 18.5 else ("Overweight" if bmi < 30 else "Obese"))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="BMI", value=f"{bmi:.2f}")
    with col2:
        st.metric(label="BMI Category", value=bmi_category)
    with col3:
        st.metric(label="Height/Weight", value=f"{height}cm / {weight}kg")
    
    # Financial Information
    st.markdown('<div class="section-header">Financial Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=6.0, step=0.1)
    
    with col2:
        occupation = st.selectbox(
            "Occupation",
            ["Business Owner", "Freelancer", "Government Job", "Private Job", "Retired", "Student", "Unemployed"]
        )
    
    # Lifestyle Information
    st.markdown('<div class="section-header">Lifestyle Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        smoker = st.selectbox("Smoker Status", ["No", "Yes"])
    
    with col2:
        city = st.text_input("City", value="Mumbai")
    
    # Calculate lifestyle risk
    lifestyle_score = 0
    if bmi < 18.5:
        lifestyle_score += 1
    elif bmi < 25:
        lifestyle_score += 2
    elif bmi < 30:
        lifestyle_score += 3
    else:
        lifestyle_score += 4
    
    lifestyle_score += 3 if smoker == "Yes" else 1
    
    if lifestyle_score <= 3:
        risk_level = "Low"
    elif lifestyle_score <= 6:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    st.markdown('<div class="section-header">Risk Assessment</div>', unsafe_allow_html=True)
    st.write(f"**Lifestyle Risk Level:** {risk_level}")
    
    st.divider()
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("Predict Premium", use_container_width=True)
    
    if predict_button:
        # Map occupation to lowercase with underscores
        occupation_map = {
            "Business Owner": "business_owner",
            "Freelancer": "freelancer",
            "Government Job": "government_job",
            "Private Job": "private_job",
            "Retired": "retired",
            "Student": "student",
            "Unemployed": "unemployed"
        }
        
        payload = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "city": city,
            "occupation": occupation_map.get(occupation, occupation.lower().replace(" ", "_"))
        }
        
        with st.spinner("Analyzing your profile..."):
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    pred_data = result.get("predicted_premium", {})
                    
                    st.success("Prediction successful!")
                    
                    # Results display
                    st.markdown('<div class="section-header">Prediction Results</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Predicted Premium",
                            f"₹{pred_data.get('prediction', 'N/A')}"
                        )
                    
                    with col2:
                        confidence = pred_data.get('confidence', 0)
                        st.metric(
                            "Confidence",
                            f"{confidence*100:.1f}%"
                        )
                    
                    with col3:
                        st.metric(
                            "Risk Category",
                            risk_level
                        )
                    
                    # Class probabilities
                    st.markdown('<div class="section-header">Premium Class Probabilities</div>', unsafe_allow_html=True)
                    
                    class_probs = pred_data.get('class_confidences', {})
                    if class_probs:
                        prob_df = pd.DataFrame({
                            'Premium Class': list(class_probs.keys()),
                            'Probability': list(class_probs.values())
                        }).sort_values('Probability', ascending=False)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.bar_chart(prob_df.set_index('Premium Class')['Probability'])
                        
                        with col2:
                            st.dataframe(
                                prob_df.assign(Probability=lambda x: x['Probability'].apply(lambda y: f"{y*100:.2f}%")),
                                use_container_width=True,
                                hide_index=True
                            )
                    
                    # Summary
                    st.markdown('<div class="section-header">Summary</div>', unsafe_allow_html=True)
                    
                    summary_data = {
                        "BMI": f"{bmi:.2f} ({bmi_category})",
                        "Risk Level": risk_level,
                        "Annual Income": f"₹{income_lpa} LPA",
                        "Prediction Confidence": f"{confidence*100:.1f}%",
                        "Predicted Premium": f"₹{pred_data.get('prediction', 'N/A')}"
                    }
                    
                    summary_df = pd.DataFrame(list(summary_data.items()), columns=["Metric", "Value"])
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)
                    
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

st.divider()
st.markdown("<p style='text-align: center; color: #999; font-size: 0.85rem;'>Insurance Premium Predictor v1.0</p>", unsafe_allow_html=True)
