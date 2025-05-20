import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(layout="wide")

# Custom CSS for the weather widget aesthetic
st.markdown(
    """
    <style>
    /* Gradient background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #3b1e5a 50%, #5e1e7d 100%);
        color: white;
        font-family: 'Arial', sans-serif;
    }

    /* Style for the title */
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }

    /* Style for the container (card) */
    .stContainer {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Style for the select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border-radius: 10px;
        border: none;
    }

    /* Style for the metrics (prediction results) */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stMetric label {
        color: #a1a1ff;
        font-size: 1.1em;
    }

    .stMetric .stMetricValue {
        color: white;
        font-size: 1.5em;
    }

    /* Style for recommendation card */
    .recommendation-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .recommendation-card p {
        color: white;
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# Tabs
tab1, _, _ = st.tabs(["📍 Prediction View", "📊 Trends (coming soon)", "🗺️ Map (coming soon)"])

with tab1:
    st.markdown("#### 🔎 Select Parameters")
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
                st.markdown('<div class="recommendation-card"><p>✅ Maintain current water management practices. Regular monitoring is recommended.</p></div>', unsafe_allow_html=True)
            elif prediction['dissolved_oxygen'] < 5:
                st.markdown('<div class="recommendation-card"><p>🚨 Urgent: Increase dissolved oxygen levels and consult environmental experts.</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="recommendation-card"><p>⚠️ Consider moderate intervention: reduce nutrients, increase aeration, and monitor closely.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="recommendation-card"><p>⚠️ No prediction available for ' + location + ' - ' + time_frame + '.</p></div>', unsafe_allow_html=True)
