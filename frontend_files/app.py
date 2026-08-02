
import streamlit as st
import pandas as pd
import os
import requests
import numpy as np

API_URL = os.environ.get("API_URL", "http://backend:7860").rstrip("/")
API_URL_PREDICT = API_URL + "/v1/predict"
API_URL_PREDICT_BATCH = API_URL + "/v1/predictbatch"

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
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Food Mart",
                                         "Supermarket Type1", "Supermarket Type2"])
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
    response = requests.post(f"{API_URL_PREDICT}", json=input_data.iloc[0].to_dict(), timeout=60)
    if response.status_code == 200:
        prediction = response.json()["Predicted_Store_Sales"]
        st.write(f"The predicted Store sale for the product is {prediction:.2f}.")
    else:
        st.error(f"API returned {response.status_code}: {response.text}")
