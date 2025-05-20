import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load precomputed data from GitHub repository
@st.cache_data
def load_data():
    site_summary = pd.read_parquet("site_summary.parquet")
    sites = pd.read_parquet("sites.parquet")['site'].tolist()
    return site_summary, sites

# Load pre-trained hybrid model
@st.cache_resource
def load_model():
    return load_model("cnn_lstm_hybrid_model.h5")

site_summary, sites = load_data()
model = load_model()

# App title and layout
st.title("Water Quality Prediction Dashboard")
st.markdown("---")

# Sidebar for location and time frame selection
st.sidebar.header("Prediction Settings")
location = st.sidebar.selectbox("Select Location", sites)
time_frame = st.sidebar.selectbox("Select Time Frame", ["Week", "Month", "Year"])

# Prediction logic
def predict_water_quality(location, time_frame):
    site_data = site_summary[site_summary['site'] == location].iloc[0]
    
    params = {
        'surface_temperature': site_data['avg_surface_temperature'],
        'middle_temperature': site_data['avg_middle_temperature'],
        'bottom_temperature': site_data['avg_bottom_temperature'],
        'ph': site_data['avg_ph'],
        'ammonia': site_data['avg_ammonia'],
        'nitrate': site_data['avg_nitrate'],
        'phosphate': site_data['avg_phosphate'],
        'dissolved_oxygen': site_data['avg_dissolved_oxygen']
    }
    
    scaler = MinMaxScaler()
    input_data = np.array(list(params.values())).reshape(1, -1)
    scaled_input = scaler.fit_transform(input_data)
    shaped_input = scaled_input.reshape(1, 1, len(params), 1)
    
    prediction = model.predict(shaped_input)
    prediction = scaler.inverse_transform(prediction)
    
    for i, param in enumerate(params.keys()):
        params[param] = prediction[0][i]
    
    wqi = (params['dissolved_oxygen'] * 0.3 + params['ph'] * 0.2 + 
           (1 - params['ammonia']) * 0.2 + (1 - params['nitrate']) * 0.15 + 
           (1 - params['phosphate']) * 0.15) * 100
    wqi_class = "Good" if wqi > 70 else "Moderate" if wqi > 50 else "Poor"
    
    return params, wqi, wqi_class

# Get predictions
params, wqi, wqi_class = predict_water_quality(location, time_frame)

# Display in a card-like format
st.subheader(f"{location} - {time_frame} Prediction")
col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://via.placeholder.com/100x150.png?text=Water+Icon", use_column_width=True)
with col2:
    st.markdown(f"<h2 style='margin: 0;'>{location}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>Temperature (Surface):</b> {params['surface_temperature']:.2f}°C</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>Dissolved Oxygen:</b> {params['dissolved_oxygen']:.2f} mg/L</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>pH:</b> {params['ph']:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>Ammonia:</b> {params['ammonia']:.2f} mg/L</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>Nitrate:</b> {params['nitrate']:.2f} mg/L</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>Phosphate:</b> {params['phosphate']:.2f} mg/L</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>WQI:</b> {wqi:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0;'><b>WQI Classification:</b> {wqi_class}</p>", unsafe_allow_html=True)

# Recommendation section
st.markdown("---")
st.subheader("Recommendation")
st.write(f"Based on the predicted WQI of {wqi:.2f} and classification '{wqi_class}', consider the following:")
if wqi_class == "Good":
    st.write("Maintain current water management practices. Regular monitoring is recommended.")
elif wqi_class == "Moderate":
    st.write("Implement moderate intervention, such as reducing nutrient input and enhancing aeration.")
else:
    st.write("Urgent action required: Reduce pollution sources, increase dissolved oxygen levels, and consult environmental experts.")
