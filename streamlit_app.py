import streamlit as st

# CSS for compact card style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    div[data-testid="stVerticalBlock"] > div:first-child {
        background: white;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        max-width: 350px;
        margin: 15px auto;
    }

    .stButton>button {
        background: linear-gradient(to bottom, #0082e0, #00c0d1);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 0.5em 1em;
        box-shadow: 0 3px 8px rgba(0, 130, 224, 0.3);
        transition: 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(to top, #00c0d1, #0082e0);
        box-shadow: 0 0 10px rgba(0, 130, 224, 0.6);
    }

    .stSelectbox>div {
        background: linear-gradient(to bottom, #0082e0, #00c0d1);
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.3em;
        margin-bottom: 10px;
    }

    .stCaption {
        text-align: center;
        color: #666;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Prediction Widget")

with st.container():
    timeframe = st.selectbox("Time Frame", ["Week", "Month", "Year"])
    location = st.selectbox("Location", [
        "Tanauan", "Talisay", "Aya", "Tumaway", "Sampaloc",
        "Berinayan", "Balakilong", "Buso-Buso", "Bañaga",
        "Bilibinwang", "Subic-Ilaya", "San Nicolas"
    ])

    if st.button("Predict"):
        image_path = f"{location.lower()}_{timeframe.lower()}_prediction.png"
        try:
            st.image(image_path, caption=f"Prediction for {location} - {timeframe}")
        except FileNotFoundError:
            st.error(f"No prediction image found for {location} - {timeframe}.")

st.caption("Last updated: May 21, 2025")
