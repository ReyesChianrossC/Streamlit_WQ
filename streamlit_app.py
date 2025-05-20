import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load precomputed data
@st.cache_data
def load_data():
    try:
        predictions = pd.read_parquet("predictions.parquet")
        if 'site' not in predictions.columns:
            st.error("Missing column: 'site'. Found: " + str(predictions.columns.tolist()))
            return None, None
        sites = predictions['site'].unique().tolist()
        return predictions, sorted(sites)
    except Exception as e:
        st.error(f"Failed to load predictions: {e}")
        return None, None

predictions, sites = load_data()
if predictions is None or sites is None:
    st.stop()

# --- UI: Main Tab ---
st.title("🌊 Water Quality Prediction Dashboard")
st.markdown("#### 📌 Main Objective: Predict water quality indicators by site and time frame")

# Tabs (only modifying the first tab as requested)
tab1, _, _ = st.tabs(["📍 Prediction View", "📊 Trends (coming soon)", "🗺️ Map (coming soon)"])

with tab1:
    st.markdown("### 🔎 Select Parameters")
    with st.container(border=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            location = st.selectbox("🌍 Select Location", sites, index=0)
        with col2:
            time_frame = st.selectbox("📅 Select Time Frame", ["Week", "Month", "Year"], index=0)

    # Fetch prediction
    def get_prediction(site, timeframe):
        result = predictions[(predictions['site'] == site) & (predictions['time_frame'] == timeframe)]
        return result.iloc[0] if not result.empty else None

    prediction = get_prediction(location, time_frame)

    if prediction is not None:
        st.markdown("### 📦 Prediction Result")
        with st.container(border=True):
            # Three-column layout for clean cards
            col1, col2, col3 = st.columns(3)

            # Column 1
            with col1:
                st.metric("🌡️ Temp (Surface)", f"{prediction['surface_temperature']:.2f} °C")
                st.metric("💧 Dissolved Oxygen", f"{prediction['dissolved_oxygen']:.2f} mg/L")
                st.metric("🧪 pH", f"{prediction['ph']:.2f}")

            # Column 2
            with col2:
                st.metric("🧫 Ammonia", f"{prediction['ammonia']:.2f} mg/L")
                st.metric("🌿 Nitrate", f"{prediction['nitrate']:.2f} mg/L")
                st.metric("🌿 Phosphate", f"{prediction['phosphate']:.2f} mg/L")

            # Column 3
            with col3:
                st.metric("📈 WQI", f"{prediction['wqi']:.2f}")
                st.metric("🏷️ Classification", prediction['wqi_classification'])

        # Recommendation Card
        st.markdown("### 🧭 Recommendation")
        with st.container(border=True):
            if prediction['wqi_classification'].lower() == "good":
                st.success("Maintain current water management practices. Regular monitoring is recommended.")
            elif prediction['dissolved_oxygen'] < 5:
                st.error("Urgent: Increase dissolved oxygen levels and consult environmental experts.")
            else:
                st.warning("Consider moderate intervention: reduce nutrients, increase aeration, and monitor closely.")
    else:
        st.warning(f"No prediction available for {location} - {time_frame}.")
