import streamlit as st
import pandas as pd

# Load precomputed data
@st.cache_data
def load_data():
    try:
        predictions = pd.read_parquet("predictions.parquet")
        sites = predictions['site'].unique().tolist()
        return predictions, sites
    except FileNotFoundError:
        st.error("Predictions file (predictions.parquet) not found. Please upload it to the repository.")
        return None, None

predictions, sites = load_data()

if predictions is None or sites is None:
    st.stop()

# App title and layout
st.title("Water Quality Prediction Dashboard")
st.markdown("---")

# Sidebar for location and time frame selection
st.sidebar.header("Prediction Settings")
location = st.sidebar.selectbox("Select Location", sites)
time_frame = st.sidebar.selectbox("Select Time Frame", ["Week", "Month", "Year"])

# Filter precomputed predictions
def get_prediction(location, time_frame):
    result = predictions[(predictions['site'] == location) & (predictions['time_frame'] == time_frame)]
    if result.empty:
        return None
    return result.iloc[0]

prediction = get_prediction(location, time_frame)

# Display in a card-like format
if prediction is not None:
    st.subheader(f"{location} - {time_frame} Prediction")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/100x150.png?text=Water+Icon", use_column_width=True)
    with col2:
        st.markdown(f"<h2 style='margin: 0;'>{location}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>Temperature (Surface):</b> {prediction['surface_temperature']:.2f}°C</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>Dissolved Oxygen:</b> {prediction['dissolved_oxygen']:.2f} mg/L</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>pH:</b> {prediction['ph']:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>Ammonia:</b> {prediction['ammonia']:.2f} mg/L</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>Nitrate:</b> {prediction['nitrate']:.2f} mg/L</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>Phosphate:</b> {prediction['phosphate']:.2f} mg/L</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>WQI:</b> {prediction['wqi']:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin: 0;'><b>WQI Classification:</b> {prediction['wqi_classification']}</p>", unsafe_allow_html=True)

    # Recommendation section
    st.markdown("---")
    st.subheader("Recommendation")
    st.write(f"Based on the predicted WQI of {prediction['wqi']:.2f} and classification '{prediction['wqi_classification']}', consider the following:")
    if prediction['wqi_classification'] == "Good":
        st.write("Maintain current water management practices. Regular monitoring is recommended.")
    elif prediction['wqi_classification'] == "Moderate":
        st.write("Implement moderate intervention, such as reducing nutrient input and enhancing aeration.")
    else:
        st.write("Urgent action required: Reduce pollution sources, increase dissolved oxygen levels, and consult environmental experts.")
else:
    st.error(f"No prediction available for {location} - {time_frame}. Please ensure the data is precomputed.")
