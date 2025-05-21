import streamlit as st

# Page config (optional)
st.set_page_config(page_title="CNN with LSTM Prediction", layout="centered")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    .vertical-box {
        height: 480px;
        width: 100%;
        max-width: 480px;
        margin: 0 auto;
        background: linear-gradient(to bottom, #0082E0, #00C0D1, #8AE7D4);
        border: 2px solid #0082E0;
        border-radius: 14px;
        box-shadow: 0 0 15px rgba(0, 130, 224, 0.6);
        padding: 24px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
    }

    .background-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('https://raw.githubusercontent.com/ReyesChianrossC/Streamlit_WQ/main/taal.png');
        background-size: cover;
        background-position: center;
        opacity: 0.1;
        z-index: 1;
    }

    .title-wrapper {
        position: absolute;
        top: 30px;
        width: 100%;
        display: flex;
        justify-content: center;
        z-index: 2;
    }

    .title {
        text-align: center;
        font-size: 29px;
        font-weight: 900;
        color: #AFD238;
        text-shadow: 0 0 8px rgba(175, 210, 56, 0.8), 1px 1px 0 #000, -1px -1px 0 #000;
    }

    .stat-comparison-button {
        position: absolute;
        top: 24px;
        right: 24px;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        border: 2px solid #00C0D1;
        background: linear-gradient(to bottom, #0082E0, #00C0D1);
        color: #E6EFEA;
        font-weight: 700;
        text-shadow: 1px 1px 0 #000;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2;
    }

    .widget-area {
        z-index: 2;
        margin-top: 300px;
        width: 100%;
    }

    .stButton>button, .stSelectbox>div {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        background: linear-gradient(to bottom, #0082E0, #00C0D1) !important;
        color: #000000 !important;
        box-shadow: 0 0 10px rgba(0, 130, 224, 0.5);
        padding: 12px 24px !important;
    }

    .chart-image {
        z-index: 2;
        margin-top: 20px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)

# HTML layout container
st.markdown("""
<div class="vertical-box">
    <div class="background-image"></div>

    <div class="stat-comparison-button">SCI</div>

    <div class="title-wrapper">
        <div class="title">CNN with LSTM Prediction</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Streamlit widgets below the styled box
st.markdown('<div class="widget-area">', unsafe_allow_html=True)

# Selectors
time_option = st.selectbox("Select Timeframe", ["Week", "Month", "Year"])
location_option = st.selectbox("Select Location", [
    "TANAUAN", "TALISAY", "AYA", "TUMAWAY", "SAMPALOC",
    "BERINAYAN", "BALAKILONG", "BUSO-BUSO", "BAÑAGA",
    "BILIBINWANG", "SUBIC-ILAYA", "SAN NICOLAS"
])

# Button
if st.button("Predict"):
    if time_option == "Week" and location_option == "TANAUAN":
        st.markdown('<div class="chart-image">', unsafe_allow_html=True)
        st.image("bar_chart_actual_values.png", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Prediction chart only available for 'Week' and 'TANAUAN'.")

st.markdown('</div>', unsafe_allow_html=True)
