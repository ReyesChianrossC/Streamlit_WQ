import streamlit as st

# CSS for container card style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=inter:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'inter', sans-serif;
    }

    div[data-testid="stverticalblock"] > div:first-child {
        background: white;
        padding: 20px 30px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 20px auto;
    }

    .stbutton>button {
        background: linear-gradient(to bottom, #0082e0, #00c0d1);
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
    .stbutton>button:hover {
        background: linear-gradient(to top, #00c0d1, #0082e0);
        box-shadow: 0 0 12px rgba(0, 130, 224, 0.7);
    }

    .stselectbox>div {
        background: linear-gradient(to bottom, #0082e0, #00c0d1);
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
    timeframe = st.selectbox("Select Time Frame", ["week", "month", "year"])
    location = st.selectbox("Select Location", [
        "tanauan", "talisay", "aya", "tumaway", "sampaloc",
        "berinayan", "balakilong", "buso-buso", "bañaga",
        "bilibinwang", "subic-ilaya", "san nicolas"
    ])

    if st.button("Predict"):
        # Debugging outputs
        st.write("Timeframe selected:", timeframe)
        st.write("Location selected:", location)

        if timeframe == "week" and location == "tanauan":
            try:
                st.image("bar_chart_actual_values.png", caption="Predicted Parameters Chart")
            except FileNotFoundError:
                st.error("Image file not found.")
        else:
            st.info(f"No chart available for {location} - {timeframe.lower()}.")

st.caption("Last updated: May 21, 2025")
