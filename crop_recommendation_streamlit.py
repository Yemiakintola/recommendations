# -*- coding: utf-8 -*-
"""crop_recommendation_streamlit

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qhkbAf61YAfo1dJg5DUiysT_xsoWTq04
"""

import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load the saved model and scaler
try:
    with open('RandomForest.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Error: 'RandomForest.pkl' not found. Please make sure the model file exists.")
    st.stop()
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Create the Streamlit web app
st.title('Crop Recommendation App')
st.header('Predict the best crop for your farm!')
st.write('Enter the details below and click the "Predict" button to see the recommended crop.')

# Input fields
try:
    n = st.number_input('Nitrogen (N)', min_value=0, max_value=140, value=50, step=1, help='Amount of nitrogen in the soil.')
    p = st.number_input('Phosphorus (P)', min_value=5, max_value=145, value=50, step=1, help='Amount of phosphorus in the soil.')
    k = st.number_input('Potassium (K)', min_value=5, max_value=205, value=50, step=1, help='Amount of potassium in the soil.')
    temperature = st.number_input('Temperature (°C)', min_value=8.825675, max_value=43.675493, value=25.0, step=0.1, help='Average temperature in your region.')
    humidity = st.number_input('Humidity (%)', min_value=14.258040, max_value=99.981876, value=60.0, step=0.1, help='Average humidity in your region.')
    ph = st.number_input('pH', min_value=3.504752, max_value=9.935091, value=7.0, step=0.1, help='pH level of the soil.')
    rainfall = st.number_input('Rainfall (mm)', min_value=20.211267, max_value=298.560117, value=100.0, step=0.1, help='Average rainfall in your region.')

    # Predict button
    if st.button('Predict'):
        # Process the input features
        input_data = np.array([[n, p, temperature, humidity, ph, rainfall, k]])

        # Scale the input features
        numerical_features = ['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall', 'K']
        input_df = pd.DataFrame(input_data, columns=numerical_features)
        scaler = StandardScaler() #need to figure out how to load the scaler
        scaled_input = scaler.fit_transform(input_df)
        scaled_input_df = pd.DataFrame(scaled_input, columns=numerical_features)

        # Make predictions
        prediction = model.predict(scaled_input_df)

        # Get predicted crop
        predicted_crops = list(y.columns[np.where(prediction[0] == True)[0]])

        # Display the prediction
        if predicted_crops:
            st.write(f'Predicted Crop(s): {", ".join(predicted_crops)}')
        else:
             st.write("No crop predicted.")

except Exception as e:
    st.error(f"An error occurred during prediction: {e}")
