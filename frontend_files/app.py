
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("store_sales_prediction_model_v1_0.joblib")

model = load_model()

# Streamlit UI for Price Prediction
st.title("SmartKart Store Sales Prediction App")
st.write("This tool predicts the SmartKart Store Sales for each product.")

st.subheader("Enter the details:")

# Collect user input
Product_Weight = st.number_input("Product Weight", min_value=0.0, step=0.1, value=12.0)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Regular", "Low Sugar", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area (ratio)", min_value=0.0, step=0.001, value=0.05, format="%.3f")
Product_Type = st.selectbox("Product Type", [
    "meat", "snack foods", "hard drinks", "dairy", "canned",
    "soft drinks", "health and hygiene", "baking goods", "bread",
    "breakfast", "frozen foods", "fruits and vegetables",
    "household", "seafood", "starchy foods", "others"
])
Product_MRP = st.number_input("Product MRP", min_value=0.0, step=1.0, value=150.0)
#Store_Id = st.selectbox("Store ID", ["OUT001", "OUT002", "OUT003", "OUT004"])
#Store_Establishment_Year = st.number_input("Store Establishment Year", min_value=1980, max_value=2025, step=1, value=2009)
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Low"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type 1", "Supermarket Type 2", "Food Mart"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    #'Store_Id': Store_Id,
    #'Store_Establishment_Year': Store_Establishment_Year,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type
}])

# Predict button
if st.button("Predict"):
    prediction = model.predict(input_data)
    st.write(f"The predicted Store sale for the product is {prediction[0]:.2f}.")
