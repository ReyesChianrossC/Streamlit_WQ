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

# Custom CSS for widget style
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #3b1e5a 50%, #5e1e7d 100%);
        color: white;
        font-family: 'Arial', sans-serif;
        padding: 10px;
    }
    .widget-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 400px;
        margin: 0 auto;
    }
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border-radius: 10px;
        border: none;
    }
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border-radius: 10px;
        border: none;
    }
    .data-item {
        margin: 5px 0;
        font-size: 1.1em;
    }
    .recommendation {
        margin-top: 15px;
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Widget container
with st.container():
    st.markdown('<div class="widget-container">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 10px;'>Water Quality Widget</h2>", unsafe_allow_html=True)

    # Controls
    location = st.selectbox("🌍 Location", sites)
    time_frame = st.selectbox("📅 Time Frame", ["Week", "Month", "Year"])
    wqi_threshold = st.slider("📊 WQI Threshold", min_value=50.0, max_value=100.0, value=70.0)
    do_threshold = st.slider("💧 DO Threshold (mg/L)", min_value=0.0, max_value=10.0, value=5.0)

    # Filter precomputed predictions
    def get_prediction(location, time_frame):
        result = predictions[(predictions['site'] == location) & (predictions['time_frame'] == time_frame)]
        return result.iloc[0] if not result.empty else None

    prediction = get_prediction(location, time_frame)

    # Display results
    if prediction is not None:
        st.markdown(f"<h3 style='text-align: center; margin: 10px 0;'>{location}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>🌡️ Temp:</b> {prediction['surface_temperature']:.2f}°C</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>💧 DO:</b> {prediction['dissolved_oxygen']:.2f} mg/L</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>🧪 pH:</b> {prediction['ph']:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>🧫 Ammonia:</b> {prediction['ammonia']:.2f} mg/L</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>🌿 Nitrate:</b> {prediction['nitrate']:.2f} mg/L</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>🌿 Phosphate:</b> {prediction['phosphate']:.2f} mg/L</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>📈 WQI:</b> {prediction['wqi']:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='data-item'><b>🏷️ Classification:</b> {prediction['wqi_classification']}</div>", unsafe_allow_html=True)

        # Recommendation
        st.markdown("<div class='recommendation'>", unsafe_allow_html=True)
        st.markdown(f"<b>🧭 Recommendation:</b> Based on WQI {prediction['wqi']:.2f} and classification '{prediction['wqi_classification']}'", unsafe_allow_html=True)
        if prediction['wqi'] >= wqi_threshold:
            st.markdown("✅ Maintain current practices. Monitor regularly.", unsafe_allow_html=True)
        elif prediction['dissolved_oxygen'] < do_threshold:
            st.markdown("🚨 Urgent: Increase oxygen levels and consult experts.", unsafe_allow_html=True)
        else:
            st.markdown("⚠️ Moderate intervention: Reduce nutrients, enhance aeration.", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='recommendation'><p>⚠️ No prediction for " + location + " - " + time_frame + ".</p></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
