import streamlit as st
import pandas as pd
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# Title
st.title("Water Quality Analysis Dashboard")

# Introduction
st.markdown("""
This dashboard displays the results of a water quality analysis, including model performance metrics and data summaries.
The metrics compare different models for predicting water quality parameters over various time horizons (Next Week, Next Month, Next Year).
""")

# Load and display combined results
st.header("Model Performance Metrics")
try:
    combined_results = pd.read_csv('combined_results.csv')
    st.dataframe(combined_results, use_container_width=True)
except FileNotFoundError:
    st.error("Error: 'combined_results.csv' not found. Please ensure the file is in the same directory as this script.")

# Load and display unique weather conditions, wind directions, and sites
st.header("Data Summaries")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Unique Weather Conditions")
    try:
        weather_conditions = pd.read_csv('weather_conditions.csv')
        st.table(weather_conditions)
    except FileNotFoundError:
        st.error("Error: 'weather_conditions.csv' not found.")

with col2:
    st.subheader("Unique Wind Directions")
    try:
        wind_directions = pd.read_csv('wind_directions.csv')
        st.table(wind_directions)
    except FileNotFoundError:
        st.error("Error: 'wind_directions.csv' not found.")

with col3:
    st.subheader("Unique Sites")
    try:
        sites = pd.read_csv('sites.csv')
        st.table(sites)
    except FileNotFoundError:
        st.error("Error: 'sites.csv' not found.")

# Display comparison plots
st.header("Model Performance Visualizations")

st.subheader("MAE Comparison")
try:
    mae_image = Image.open('mae_comparison.png')
    st.image(mae_image, caption="MAE Comparison Across Models", use_column_width=True)
except FileNotFoundError:
    st.error("Error: ' Mae_comparison.png' not found.")

st.subheader("MSE Comparison")
try:
    mse_image = Image.open('mse_comparison.png')
    st.image(mse_image, caption="MSE Comparison Across Models", use_column_width=True)
except FileNotFoundError:
    st.error("Error: 'mse_comparison.png' not found.")

st.subheader("RMSE Comparison")
try:
    rmse_image = Image.open('rmse_comparison.png')
    st.image(rmse_image, caption="RMSE Comparison Across Models", use_column_width=True)
except FileNotFoundError:
    st.error("Error: 'rmse_comparison.png' not found.")

st.subheader("R2 Score Comparison")
try:
    r2_image = Image.open('r2_comparison.png')
    st.image(r2_image, caption="R2 Score Comparison Across Models", use_column_width=True)
except FileNotFoundError:
    st.error("Error: 'r2_comparison.png' not found.")

# Footer
st.markdown("""
---
**CPEN 106 - GROUP 1**
Members:
Agana
Casa
Gregorio
Jeremillos
Reyes
""")
