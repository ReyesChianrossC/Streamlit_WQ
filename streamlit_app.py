import streamlit as st
import pandas as pd

# Load precomputed data
@st.cache_data
def load_data():
    try:
        predictions = pd.read_parquet("predictions.parquet")
        st.write("Loaded columns:", predictions.columns.tolist())  # Debug: Print columns
        if 'site' not in predictions.columns:
            st.error("Column 'site' not found in predictions.parquet. Available columns are: " + str(predictions.columns.tolist()))
            return None, None
        sites = predictions['site'].unique().tolist()
        return predictions, sites
    except FileNotFoundError:
        st.error("Predictions file (predictions.parquet) not found. Please upload it to the repository.")
        return None, None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

predictions, sites = load_data()

if predictions is None or sites is None:
    st.stop()

# App title
st.title("Water Quality Prediction Dashboard")
st.markdown("---")

# Create a two-column layout: left for controls, right for results
col1, col2 = st.columns([1, 2])

# Left column: All controls in a single box
with col1:
    with st.container(border=True):
        st.header("Prediction Settings")
        location = st.selectbox("Select Location", sites)
        time_frame = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])
        # Add sliders (example: adjust thresholds for WQI)
        wqi_threshold = st.slider("WQI Threshold for 'Good'", min_value=50.0, max_value=100.0, value=70.0)
        do_threshold = st.slider("Dissolved Oxygen Threshold (mg/L)", min_value=0.0, max_value=10.0, value=5.0)

# Filter precomputed predictions
def get_prediction(location, time_frame):
    result = predictions[(predictions['site'] == location) & (predictions['time_frame'] == time_frame)]
    if result.empty:
        return None
    return result.iloc[0]

prediction = get_prediction(location, time_frame)

# Right column: Display results
with col2:
    if prediction is not None:
        st.subheader(f"{location} - {time_frame} Prediction")
        # Card-like display
        col_img, col_text = st.columns([1, 2])
        with col_img:
            st.image("https://via.placeholder.com/100x150.png?text=Water+Icon", use_container_width=True)
        with col_text:
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
        if prediction['wqi'] >= wqi_threshold:
            st.write("Maintain current water management practices. Regular monitoring is recommended.")
        elif prediction['dissolved_oxygen'] < do_threshold:
            st.write("Urgent action required: Increase dissolved oxygen levels and consult environmental experts.")
        else:
            st.write("Implement moderate intervention, such as reducing nutrient input and enhancing aeration.")
    else:
        st.error(f"No prediction available for {location} - {time_frame}. Please ensure the data is precomputed.")
