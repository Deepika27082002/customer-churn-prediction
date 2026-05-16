import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
model = joblib.load("models/model.pkl")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
📊 Customer Churn Prediction Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align: center;'>
Telecom Customer Retention & Churn Analysis System
</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Model",
        value="XGBoost"
    )

with col2:
    st.metric(
        label="ROC-AUC",
        value="0.816"
    )

with col3:
    st.metric(
        label="Recall",
        value="0.57"
    )

st.markdown("---")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📌 Customer Input Panel")

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

senior = st.sidebar.selectbox(
    "Senior Citizen",
    [0, 1]
)

partner = st.sidebar.selectbox(
    "Partner",
    ["Yes", "No"]
)

dependents = st.sidebar.selectbox(
    "Dependents",
    ["Yes", "No"]
)

tenure = st.sidebar.slider(
    "Tenure (Months)",
    0,
    72,
    12
)

phone_service = st.sidebar.selectbox(
    "Phone Service",
    ["Yes", "No"]
)

multiple_lines = st.sidebar.selectbox(
    "Multiple Lines",
    ["Yes", "No", "No phone service"]
)

internet_service = st.sidebar.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

online_security = st.sidebar.selectbox(
    "Online Security",
    ["Yes", "No", "No internet service"]
)

online_backup = st.sidebar.selectbox(
    "Online Backup",
    ["Yes", "No", "No internet service"]
)

device_protection = st.sidebar.selectbox(
    "Device Protection",
    ["Yes", "No", "No internet service"]
)

tech_support = st.sidebar.selectbox(
    "Tech Support",
    ["Yes", "No", "No internet service"]
)

streaming_tv = st.sidebar.selectbox(
    "Streaming TV",
    ["Yes", "No", "No internet service"]
)

streaming_movies = st.sidebar.selectbox(
    "Streaming Movies",
    ["Yes", "No", "No internet service"]
)

contract = st.sidebar.selectbox(
    "Contract Type",
    ["Month-to-month", "One year", "Two year"]
)

paperless = st.sidebar.selectbox(
    "Paperless Billing",
    ["Yes", "No"]
)

payment_method = st.sidebar.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly_charges = st.sidebar.slider(
    "Monthly Charges",
    0,
    150,
    70
)

total_charges = st.sidebar.number_input(
    "Total Charges",
    0.0,
    10000.0,
    1000.0
)

# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------
charge_ratio = monthly_charges / (tenure + 1)

if tenure <= 12:
    tenure_group = "0-1 Year"

elif tenure <= 24:
    tenure_group = "1-2 Years"

elif tenure <= 48:
    tenure_group = "2-4 Years"

else:
    tenure_group = "4+ Years"

# ---------------------------------------------------
# INPUT DATA
# ---------------------------------------------------
input_dict = {

    "SeniorCitizen": senior,

    "tenure": tenure,

    "PhoneService":
        1 if phone_service == "Yes" else 0,

    "OnlineSecurity":
        1 if online_security == "Yes" else 0,

    "OnlineBackup":
        1 if online_backup == "Yes" else 0,

    "DeviceProtection":
        1 if device_protection == "Yes" else 0,

    "TechSupport":
        1 if tech_support == "Yes" else 0,

    "StreamingTV":
        1 if streaming_tv == "Yes" else 0,

    "StreamingMovies":
        1 if streaming_movies == "Yes" else 0,

    "MonthlyCharges": monthly_charges,

    "TotalCharges": total_charges,

    "TotalServices": (
        (1 if phone_service == "Yes" else 0) +
        (1 if online_security == "Yes" else 0) +
        (1 if online_backup == "Yes" else 0) +
        (1 if device_protection == "Yes" else 0) +
        (1 if tech_support == "Yes" else 0) +
        (1 if streaming_tv == "Yes" else 0) +
        (1 if streaming_movies == "Yes" else 0)
    ),

    "ChargeRatio": charge_ratio,

    "gender_Male":
        1 if gender == "Male" else 0,

    "Partner_Yes":
        1 if partner == "Yes" else 0,

    "Dependents_Yes":
        1 if dependents == "Yes" else 0,

    "MultipleLines_No phone service":
        1 if multiple_lines == "No phone service" else 0,

    "MultipleLines_Yes":
        1 if multiple_lines == "Yes" else 0,

    "InternetService_Fiber optic":
        1 if internet_service == "Fiber optic" else 0,

    "InternetService_No":
        1 if internet_service == "No" else 0,

    "Contract_One year":
        1 if contract == "One year" else 0,

    "Contract_Two year":
        1 if contract == "Two year" else 0,

    "PaperlessBilling_Yes":
        1 if paperless == "Yes" else 0,

    "PaymentMethod_Credit card (automatic)":
        1 if payment_method == "Credit card (automatic)" else 0,

    "PaymentMethod_Electronic check":
        1 if payment_method == "Electronic check" else 0,

    "PaymentMethod_Mailed check":
        1 if payment_method == "Mailed check" else 0,

    "TenureGroup_1-2 Years":
        1 if tenure_group == "1-2 Years" else 0,

    "TenureGroup_2-4 Years":
        1 if tenure_group == "2-4 Years" else 0,

    "TenureGroup_4+ Years":
        1 if tenure_group == "4+ Years" else 0
}

input_df = pd.DataFrame([input_dict])

# ---------------------------------------------------
# PREDICTION
# ---------------------------------------------------
if st.button("🔍 Predict Churn"):

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]

    st.markdown("---")

    st.subheader("📈 Prediction Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )

    with col2:

        if prediction == 1:
            st.error("⚠ High Churn Risk")

        else:
            st.success("✅ Low Churn Risk")

    # ---------------------------------------------------
    # PROGRESS BAR
    # ---------------------------------------------------
    st.progress(float(probability))

    # ---------------------------------------------------
    # RISK LEVEL
    # ---------------------------------------------------
    if probability > 0.75:

        st.error("🔴 High Risk Customer")

    elif probability > 0.50:

        st.warning("🟠 Medium Risk Customer")

    else:

        st.success("🟢 Low Risk Customer")

    # ---------------------------------------------------
    # BUSINESS INSIGHTS
    # ---------------------------------------------------
    st.subheader("📊 Business Insights")

    if contract == "Month-to-month":
        st.warning(
            "Month-to-month customers show high churn tendency."
        )

    if monthly_charges > 80:
        st.warning(
            "High monthly charges may increase churn risk."
        )

    if tenure < 12:
        st.warning(
            "New customers are more likely to churn."
        )

    if payment_method == "Electronic check":
        st.warning(
            "Electronic check users historically show higher churn."
        )

    # ---------------------------------------------------
    # RETENTION RECOMMENDATIONS
    # ---------------------------------------------------
    st.subheader("💡 Recommended Retention Actions")

    if probability > 0.75:

        st.write("• Offer loyalty discount")
        st.write("• Suggest yearly contract")
        st.write("• Provide premium support")
        st.write("• Give personalized retention offer")

    elif probability > 0.50:

        st.write("• Send promotional offers")
        st.write("• Improve customer engagement")
        st.write("• Monitor customer satisfaction")

    else:

        st.write("• Customer appears stable")
        st.write("• Continue standard engagement")

# ---------------------------------------------------
# DASHBOARD SECTION
# ---------------------------------------------------
st.markdown("---")

st.subheader("📉 Top Churn Risk Drivers")

chart_data = pd.DataFrame({
    "Feature": [
        "Month-to-Month",
        "Fiber Optic",
        "Electronic Check",
        "High Charges",
        "Low Tenure"
    ],
    "RiskScore": [
        90,
        75,
        65,
        80,
        85
    ]
})

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=chart_data,
    x="RiskScore",
    y="Feature",
    ax=ax
)

plt.title("Top Churn Risk Drivers")

st.pyplot(fig)

# ---------------------------------------------------
# SHAP IMAGE
# ---------------------------------------------------
st.markdown("---")

st.subheader("🧠 SHAP Explainability")

st.image(
    "notebooks/shap_summary.png",
    caption="Feature Impact on Churn Prediction"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.write(
    "Built using Streamlit, XGBoost, SHAP, and Machine Learning"
)