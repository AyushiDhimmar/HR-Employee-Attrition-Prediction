import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("hr_model.joblib")

st.set_page_config(
    page_title="Employee Attrition Prediction",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Employee Attrition Prediction")
st.write("Predict whether an employee is likely to leave the company.")

st.subheader("Employee Information")

st.sidebar.title("About Project")

st.sidebar.info("""
Machine Learning project that predicts employee attrition using HR analytics data.

Models Used:
- Logistic Regression
- Decision Tree Classifier

Best Accuracy: 93.38%
""")

st.sidebar.title("Project Overview")

st.sidebar.metric("Dataset Size", "1,470 Records")
st.sidebar.metric("Best Accuracy", "93.38%")
st.sidebar.metric("Best Model", "Decision Tree")
# Numerical Inputs
age = st.number_input("Age", min_value=18, max_value=65, value=30)
salary = st.number_input(
    "Monthly Salary",
    min_value=1000,
    value=50000
)
years_at_company = st.number_input("Years At Company", min_value=0, max_value=40, value=5)
distance_from_home = st.number_input(
    "Distance From Home (km)",
    min_value=1,
    max_value=50,
    value=10
)

# Categorical Inputs
gender = st.selectbox("Gender", ["Male", "Female"])

job_satisfaction_text = st.select_slider(
    "Job Satisfaction",
    options=["Low", "Medium", "High", "Very High"]
)

job_satisfaction = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Very High": 4
}[job_satisfaction_text]

work_life_text = st.select_slider(
    "Work-Life Balance",
    options=["Poor", "Fair", "Good", "Excellent"]
)

work_life_balance = {
    "Poor": 1,
    "Fair": 2,
    "Good": 3,
    "Excellent": 4
}[work_life_text]

education = st.selectbox(
    "Education Level",
    [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "Doctorate"
    ]
)

education_level = {
    "High School": 1,
    "Diploma": 2,
    "Bachelor's": 3,
    "Master's": 4,
    "Doctorate": 5
}[education]

performance = st.selectbox(
    "Performance Rating",
    ["Poor", "Average", "Good", "Excellent"]
)

performance_rating = {
    "Poor": 1,
    "Average": 2,
    "Good": 3,
    "Excellent": 4
}[performance]

overtime = st.selectbox(
    "Overtime",
    ["No", "Yes"]
)

job_role = st.selectbox(
    "Job Role",
    ["HR", "Manager", "Sales", "Technician"]
)

marital_status = st.selectbox(
    "Marital Status",
    ["Single", "Married"]
)

if st.button("Predict Attrition"):

    gender = 1 if gender == "Male" else 0
    overtime = 1 if overtime == "Yes" else 0

    input_data = pd.DataFrame({
        "Age": [age],
        "Gender": [gender],
        "Salary": [salary],
        "JobSatisfaction": [job_satisfaction],
        "WorkLifeBalance": [work_life_balance],
        "YearsAtCompany": [years_at_company],
        "Overtime": [overtime],
        "DistanceFromHome": [distance_from_home],
        "EducationLevel": [education_level],
        "PerformanceRating": [performance_rating],
        "JobRole_HR": [1 if job_role == "HR" else 0],
        "JobRole_Manager": [1 if job_role == "Manager" else 0],
        "JobRole_Sales": [1 if job_role == "Sales" else 0],
        "JobRole_Technician": [1 if job_role == "Technician" else 0],
        "MaritalStatus_Married": [1 if marital_status == "Married" else 0],
        "MaritalStatus_Single": [1 if marital_status == "Single" else 0]
    })

    prediction = model.predict(input_data)[0]

    st.markdown("---")

    reasons = []

    if prediction == 1:

        st.error("⚠️ Employee is Likely to Leave")

        st.subheader("Top Factors Contributing to Attrition Risk")

        if overtime == 1:
            reasons.append("Overtime is enabled")

        if job_satisfaction <= 2:
            reasons.append("Low job satisfaction")

        if work_life_balance <= 2:
            reasons.append("Poor work-life balance")

        if salary < 40000:
            reasons.append("Lower salary level")

        if years_at_company < 3:
            reasons.append("Short tenure at company")

        if distance_from_home > 20:
            reasons.append("Long commuting distance")

    else:

        st.success("✅ Employee is Likely to Stay")

        st.subheader("Top Factors Supporting Retention")

        if overtime == 0:
            reasons.append("No overtime requirement")

        if job_satisfaction >= 3:
            reasons.append("High job satisfaction")

        if work_life_balance >= 3:
            reasons.append("Good work-life balance")

        if salary >= 50000:
            reasons.append("Competitive salary")

        if years_at_company >= 5:
            reasons.append("Strong company tenure")

        if distance_from_home <= 10:
            reasons.append("Convenient commuting distance")

        if marital_status == "Married":
            reasons.append("Stable personal profile")

    for i, reason in enumerate(reasons[:5], 1):
        st.write(f"{i}. {reason}")

    st.subheader("Prediction Summary")

    st.write(f"Age: {age}")
    st.write(f"Monthly Salary: ₹{salary:,}")
    st.write(f"Years At Company: {years_at_company}")
    st.write(f"Job Role: {job_role}")
    st.write(f"Education Level: {education}")
    st.write(f"Performance Rating: {performance}")
    st.write(f"Marital Status: {marital_status}")

st.markdown("---")
st.caption("Developed by Ayushi Dhimmar")