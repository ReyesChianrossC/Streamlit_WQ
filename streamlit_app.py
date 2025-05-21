import streamlit as st

# CSS for container card style
st.markdown("""
<style>
    /* Apply font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Style the Streamlit container */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background: white;
        padding: 20px 30px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 20px auto;
    }

    /* Buttons styling */
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

    /* Selectbox style */
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

with st.container():
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

st.caption("Last updated: May 21, 2025")
