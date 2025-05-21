import streamlit as st
import pandas as pd
import altair as alt

# Streamlit config
st.set_page_config(page_title="Water Quality Dashboard", layout="wide")

# === Custom CSS for Dark Dashboard ===
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
</style>
""", unsafe_allow_html=True)

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
