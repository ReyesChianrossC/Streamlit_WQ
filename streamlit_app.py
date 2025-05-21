import streamlit as st

# Basic CSS styling for widgets and container card
st.markdown("""
<style>
    /* Apply custom font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Card container styling */
    .card-container {
        background: white;
        padding: 20px 30px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 20px auto;
    }

    .stButton>button {
        background: linear-gradient(to bottom, #0082E0, #00C0D1);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        box-shadow: 0 4px 10px rgba(0, 130, 224, 0.4);
        transition: 0.3s ease;
        width: 100%;
        margin-top: 12px;
    }

    .stButton>button:hover {
        background: linear-gradient(to top, #00C0D1, #0082E0);
        box-shadow: 0 0 12px rgba(0, 130, 224, 0.7);
    }

    .stSelectbox>div {
        background: linear-gradient(to bottom, #0082E0, #00C0D1);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.4em;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("CNN with LSTM Prediction")

# Start container div
st.markdown('<div class="card-container">', unsafe_allow_html=True)

timeframe = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])
location = st.selectbox("Select Location", [
    "TANAUAN", "TALISAY", "AYA", "TUMAWAY", "SAMPALOC",
    "BERINAYAN", "BALAKILONG", "BUSO-BUSO", "BAÑAGA",
    "BILIBINWANG", "SUBIC-ILAYA", "SAN NICOLAS"
])

if st.button("Predict"):
    if timeframe == "Week" and location == "TANAUAN":
        st.image("bar_chart_actual_values.png", caption="Predicted Parameters Chart")
    else:
        st.info(f"No chart available for {location} - {timeframe.lower()}.")

# End container div
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Last updated: May 21, 2025")
