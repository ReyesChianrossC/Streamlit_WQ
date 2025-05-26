```python
import streamlit as st
import pandas as pd
import altair as alt

# Streamlit config
st.set_page_config(page_title="Water Quality Dashboard", layout="wide")

# Initialize session state for popup
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False

# === Custom CSS for Dark Dashboard and Button ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #1e1e2f;
    color: #f1f1f1;
}

h1, h2, h3 {
    color: #f8f9fa;
}

.section {
    background-color: #2c2c3e;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    margin-bottom: 30px;
}

.stat-block {
    background-color: #2c2c3e;
    color: #f1f1f1;
    border-left: 4px solid #6f42c1;
    padding: 12px 16px;
    margin-bottom: 10px;
    border-radius: 6px;
}

.sidebar .css-1d391kg {
    background-color: #29293f !important;
}

.metric-title {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 3px;
    color: #f1f1f1;
}

.metric-value {
    font-family: monospace;
    font-size: 0.9rem;
    color: #bcbcff;
}

/* Floating Button */
.floating-button {
    position: fixed;
    top: 10px;
    right: 10px;
    width: 128px;
    height: 128px;
    background-color: #6f42c1;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    z-index: 1000;
}

/* Popup Styling */
.popup-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #2c2c3e;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    z-index: 2000;
    width: 900px; /* Adjusted for three facets */
    max-height: 500px; /* Reduced height for compactness */
    overflow-y: auto; /* Allow scrolling */
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# === Floating Button ===
st.markdown("""
<div class='floating-button' onclick='st.session_state.show_popup=True'>
    <span style='color: #f1f1f1; font-size: 1.2rem; font-weight: bold;'>Model Comparison</span>
</div>
""", unsafe_allow_html=True)

# === Popup Logic ===
if st.session_state.show_popup:
    with st.container():
        st.markdown("""
        <div class='popup-container'>
            <h3>Model Performance Comparison</h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load model comparison data
            comparison_df = pd.read_parquet("model_comparison.parquet")
            
            # Validate data
            if comparison_df.empty:
                st.markdown("""
                <div class='popup-container'>
                    <p>No data found in model_comparison.parquet.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Create Altair bar chart
                chart = alt.Chart(comparison_df).mark_bar().encode(
                    x=alt.X('model:N', title='Model', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('mae:Q', title='Mean Absolute Error', scale=alt.Scale(domain=[0, comparison_df['mae'].max() * 1.2])),
                    color=alt.condition(
                        alt.datum.best_model,
                        alt.value('#6f42c1'),  # Highlight best model
                        alt.value('#a29bfe')
                    ),
                    column=alt.Column('prediction_gap:N', title='Prediction Gap'),
                    tooltip=['model', 'prediction_gap', alt.Tooltip('mae', format='.6f')]
                ).properties(
                    width=250,  # Slightly wider facets
                    height=300
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                )
                
                # Display chart in popup
                with st.container():
                    st.altair_chart(chart, use_container_width=True)
                
        except FileNotFoundError:
            st.markdown("""
            <div class='popup-container'>
                <p>model_comparison.parquet not found.</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class='popup-container'>
                <p>Error loading chart: {e}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Close button
        with st.container():
            if st.button("Close Popup", key="close_popup"):
                st.session_state.show_popup = False

# === Sidebar ===
st.sidebar.title("Navigation")
location = st.sidebar.selectbox("Select Location", [
    "TANAUAN", "TALISAY", "AYA", "TUMAWAY", "SAMPALOC",
    "BERINAYAN", "BALAKILONG", "BUSO-BUSO", "BAÑAGA",
    "BILIBINWANG", "SUBIC-ILAYA", "SAN NICOLAS"
])

timeframe = st.sidebar.selectbox("Select Time Frame", ["Week", "Month", "Year"])

# === Load data ===
try:
    df = pd.read_parquet("predictions.parquet")
except FileNotFoundError:
    st.error("Missing predictions.parquet file.")
    st.stop()

# === Filter & Compute ===
try:
    selected_df = df[(df['site'] == location) & (df['time_frame'] == timeframe)]
    if selected_df.empty:
        st.error("No matching data found.")
        st.stop()
    selected = selected_df.iloc[0]

    baseline_df = df[(df['site'] == location) & (df['time_frame'] == timeframe)]
    baseline = baseline_df.mean(numeric_only=True)
except Exception as e:
    st.error(f"Data processing error: {e}")
    st.stop()

# === Header ===
st.title("Water Quality Dashboard")
st.subheader(f"{location} • {timeframe} View")

# === Top Metrics ===
metrics = {
    "WQI": 'wqi',
    "pH": 'ph',
    "DO (mg/L)": 'dissolved_oxygen',
    "Ammonia": 'ammonia'
}

cols = st.columns(len(metrics))

for i, (label, key) in enumerate(metrics.items()):
    value = selected[key]
    base = baseline[key]
    delta = round(value - base, 2)
    if delta > 0:
        cols[i].metric(label, f"{value:.2f}", f"↑ {delta:.2f}", delta_color="normal")
    elif delta < 0:
        cols[i].metric(label, f"{value:.2f}", f"↓ {abs(delta):.2f}", delta_color="normal")
    else:
        cols[i].metric(label, f"{value:.2f}", f"{delta:.2f}", delta_color="off")

# === Tabs ===
tab1, tab2 = st.tabs(["Prediction Overview", "Parameter Comparison"])

with tab1:
    st.markdown("### Predicted Water Quality Changes")

    param_map = {
        'Surface Temp': 'surface_temperature',
        'Middle Temp': 'middle_temperature',
        'Bottom Temp': 'bottom_temperature',
        'pH': 'ph',
        'Ammonia': 'ammonia',
        'Nitrate': 'nitrate',
        'Phosphate': 'phosphate',
        'Diss. Oxygen': 'dissolved_oxygen',
        'WQI': 'wqi'
    }

    for name, key in param_map.items():
        before = baseline[key]
        after = selected[key]
        st.markdown(f"""
        <div class='stat-block'>
            <div class='metric-title'>{name}</div>
            <div class='metric-value'>[{before:.4f}] → [{after:.4f}]</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='margin-top: 20px; font-size: 1.1rem;'>
            <strong>WQI Classification:</strong> {selected['wqi_classification']}
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### Parameter Comparison Chart")
    chart_data = pd.DataFrame({
        "Parameter": list(param_map.keys()),
        "Baseline": [baseline[k] for k in param_map.values()],
        "Predicted": [selected[k] for k in param_map.values()]
    })

    melted = chart_data.melt(id_vars="Parameter", var_name="Type", value_name="Value")

    chart = alt.Chart(melted).mark_bar(opacity=0.85).encode(
        x=alt.X('Parameter:N', title=None),
        y=alt.Y('Value:Q'),
        color=alt.Color('Type:N', scale=alt.Scale(range=['#a29bfe', '#6c5ce7'])),
        tooltip=['Parameter', 'Type', 'Value']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

# === Footer ===
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("CPEN106 • Water Quality Monitoring • Updated: May 21, 2025")
