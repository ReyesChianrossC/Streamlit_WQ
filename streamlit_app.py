import streamlit as st
import pandas as pd

# ✅ Set page config early
st.set_page_config(
    page_title="Water Quality Prediction",
    layout="centered"  # ⬅️ Makes it a compact single-box look
)

# ✅ Load data
@st.cache_data
def load_data():
    try:
        predictions = pd.read_parquet("predictions.parquet")
        if 'site' not in predictions.columns:
            st.error("Column 'site' not found. Available columns: " + str(predictions.columns.tolist()))
            return None, None
        sites = predictions['site'].unique().tolist()
        return predictions, sites
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

predictions, sites = load_data()
if predictions is None or sites is None:
    st.stop()

# ✅ UI Title
st.markdown("## 💧 Water Quality Prediction")
st.markdown("### 🧪 Select location and time frame to predict parameters")
st.markdown("---")

# ✅ Unified box-style UI container
with st.container(border=True):
    # Input controls
    st.markdown("### 🎛️ Settings")
    location = st.selectbox("📍 Select Location", sites)
    time_frame = st.selectbox("🕒 Select Time Frame", ["Week", "Month", "Year"])
    wqi_threshold = st.slider("✅ WQI Threshold (Good)", 50.0, 100.0, 70.0)
    do_threshold = st.slider("💧 DO Threshold (mg/L)", 0.0, 10.0, 5.0)

    # Fetch prediction
    def get_prediction(location, time_frame):
        result = predictions[(predictions['site'] == location) & (predictions['time_frame'] == time_frame)]
        return result.iloc[0] if not result.empty else None

    prediction = get_prediction(location, time_frame)

    st.markdown("---")

    if prediction is not None:
        # Display results in a nice card layout
        st.markdown(f"### 📊 Results for **{location}** ({time_frame})")
        colA, colB = st.columns([1, 2])
        with colA:
            st.image("https://via.placeholder.com/100x150.png?text=Water+Icon", use_container_width=True)

        with colB:
            st.markdown(f"**🌡️ Temp (Surface):** {prediction['surface_temperature']:.2f} °C")
            st.markdown(f"**💧 Dissolved Oxygen:** {prediction['dissolved_oxygen']:.2f} mg/L")
            st.markdown(f"**🧪 pH:** {prediction['ph']:.2f}")
            st.markdown(f"**🧫 Ammonia:** {prediction['ammonia']:.2f} mg/L")
            st.markdown(f"**🌿 Nitrate:** {prediction['nitrate']:.2f} mg/L")
            st.markdown(f"**🌿 Phosphate:** {prediction['phosphate']:.2f} mg/L")
            st.markdown(f"**📈 WQI:** {prediction['wqi']:.2f}")
            st.markdown(f"**🏷️ Classification:** {prediction['wqi_classification']}")

        # Recommendation section
        st.markdown("---")
        st.markdown("### 🧭 Recommendation")
        if prediction['wqi'] >= wqi_threshold:
            st.success("Maintain current water management practices. Regular monitoring is recommended.")
        elif prediction['dissolved_oxygen'] < do_threshold:
            st.error("Urgent: Increase DO levels and consult environmental experts.")
        else:
            st.warning("Consider moderate intervention: reduce nutrients, enhance aeration, monitor closely.")
    else:
        st.warning(f"No prediction available for {location} - {time_frame}.")
