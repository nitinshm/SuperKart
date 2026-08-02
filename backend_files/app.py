import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
superkart_api = Flask("SuperKart Store Sales Predictor")

# Load the trained Boston housing model
model = joblib.load("store_sales_prediction_model_v1_0.joblib")

# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Store Sales Prediction API!"


# Define an endpoint to predict price for a single house
@superkart_api.post('/v1/predict')
def predict_superkart():
    # Get JSON data from the request
    superkart_data = request.get_json()

    # Extract relevant superkart features from the input data
    sample = {
        'Product_Weight': superkart_data['Product_Weight'],
        'Product_Allocated_Area': superkart_data['Product_Allocated_Area'],
        'Product_MRP': superkart_data['Product_MRP'],
        'Store_Age_Years': superkart_data['Store_Age_Years'],
        'Product_Sugar_Content': superkart_data['Product_Sugar_Content'],     
        'Store_Location_City_Type': superkart_data['Store_Location_City_Type'],
        'Store_Type': superkart_data['Store_Type'],
        'Product_Id_char': superkart_data['Product_Id_char'],
        'Product_Type_Category': superkart_data['Product_Type_Category'],
        }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_MEDV': prediction})

# Define an endpoint to predict price for a batch of houses
@superkart_api.post('/v1/predictbatch')
def predict_superkart_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Predicted_MEDV'] = predictions

    # Convert results to dictionary
    result = input_data.to_dict(orient="records")

    return jsonify(result)

# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
