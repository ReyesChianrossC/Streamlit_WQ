import streamlit as st

# Basic CSS styling for widgets
st.markdown("""
<style>
    /* Apply custom font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
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
    }

    .stButton>button:hover {
        background: linear-gradient(to top, #00C0D1, #0082E0);
        box-shadow: 0 0 12px rgba(0, 130, 224, 0.7);
    }

    .stSelectbox>div {
        background: linear-gradient(to bottom, #0082E0, #00C0D1);
        color: black;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.4em;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit widgets
st.title("CNN with LSTM Prediction")

timeframe = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])
location = st.selectbox("Select Location", [
    "TANAUAN", "TALISAY", "AYA", "TUMAWAY", "SAMPALOC",
    "BERINAYAN", "BALAKILONG", "BUSO-BUSO", "BAÑAGA",
    "BILIBINWANG", "SUBIC-ILAYA", "SAN NICOLAS"
])

# Predict button
if st.button("Predict"):
    # Example logic: show result or image
    if timeframe == "Week" and location == "TANAUAN":
        st.image("bar_chart_actual_values.png", caption="Predicted Parameters Chart")
    else:
        st.info(f"No chart available for {location} - {timeframe.lower()}.")

# Optional footer
st.caption("Last updated: May 21, 2025")
