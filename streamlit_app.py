import streamlit as st
import pandas as pd

# Load precomputed data
@st.cache_data
def load_data():
    try:
        predictions = pd.read_parquet("predictions.parquet")
        if 'site' not in predictions.columns:
            st.error("Column 'site' not found in predictions.parquet. Available columns: " + str(predictions.columns.tolist()))
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

# Layout: Controls and Results
col1, col2 = st.columns([1, 2])

# --- LEFT: Compact control panel ---
with col1:
    with st.container(border=True):
        st.header("Prediction Settings")
        location = st.selectbox("Select Location", sites)
        time_frame = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])
        wqi_threshold = st.slider("WQI Threshold for 'Good'", min_value=50.0, max_value=100.0, value=70.0)
        do_threshold = st.slider("Dissolved Oxygen Threshold (mg/L)", min_value=0.0, max_value=10.0, value=5.0)

# --- RIGHT: Prediction Results ---
def get_prediction(location, time_frame):
    result = predictions[(predictions['site'] == location) & (predictions['time_frame'] == time_frame)]
    if result.empty:
        return None
    return result.iloc[0]

prediction = get_prediction(location, time_frame)

with col2:
    if prediction is not None:
        st.subheader(f"{location} - {time_frame} Prediction")
        
        # Display prediction results
        st.markdown(f"**Temperature (Surface):** {prediction['surface_temperature']:.2f}°C")
        st.markdown(f"**Dissolved Oxygen:** {prediction['dissolved_oxygen']:.2f} mg/L")
        st.markdown(f"**pH:** {prediction['ph']:.2f}")
        st.markdown(f"**Ammonia:** {prediction['ammonia']:.2f} mg/L")
        st.markdown(f"**Nitrate:** {prediction['nitrate']:.2f} mg/L")
        st.markdown(f"**Phosphate:** {prediction['phosphate']:.2f} mg/L")
        st.markdown(f"**WQI:** {prediction['wqi']:.2f}")
        st.markdown(f"**WQI Classification:** {prediction['wqi_classification']}")

        # Recommendation section
        st.markdown("---")
        st.subheader("Recommendation")
        st.write(f"Based on the predicted WQI of {prediction['wqi']:.2f} and classification '{prediction['wqi_classification']}', consider the following:")

        if prediction['wqi'] >= wqi_threshold:
            st.success("Maintain current water management practices. Regular monitoring is recommended.")
        elif prediction['dissolved_oxygen'] < do_threshold:
            st.error("Urgent action required: Increase dissolved oxygen levels and consult environmental experts.")
        else:
            st.warning("Implement moderate intervention, such as reducing nutrient input and enhancing aeration.")
    else:
        st.error(f"No prediction available for {location} - {time_frame}. Please ensure the data is precomputed.")
