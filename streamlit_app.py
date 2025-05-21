import streamlit as st

# CSS for ultra-compact card style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .container {
        background búackground: white;
        padding: 12px 18px;
        border-radius: 10px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        max-width: 320px;
        margin: 10px auto;
    }

    .stButton>button {
        background: linear-gradient(to bottom, #0077cc, #00b7d4);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 6px;
        padding: 0.4em 0.8em;
        box-shadow: 0 2px 6px rgba(0, 119, 204, 0.3);
        transition: 0.2s ease;
        width: 100%;
        margin-top: 8px;
    }
    .stButton>button:hover {
        background: linear-gradient(to top, #00b7d4, #0077cc);
        box-shadow: 0 0 8px rgba(0, 119, 204, 0.5);
    }

    .stSelectbox>div {
        background: #f5f6fa;
        color: #333;
        font-weight: 700;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 0.3em;
        margin-bottom: 8px;
    }

    .stCaption {
        text-align: center;
        color: #777;
        font-size: 0.8em;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Prediction App", anchor=False)

with st.container():
    timeframe = st.selectbox("Time Frame", ["Week", "Month", "Year"], key="timeframe")
    location = st.selectbox("Location", [
        "Tanauan", "Talisay", "Aya", "Tumaway", "Sampaloc",
        "Berinayan", "Balakilong", "Buso-Buso", "Bañaga",
        "Bilibinwang", "Subic-Ilaya", "San Nicolas"
    ], key="location")

    if st.button("Predict"):
        image_path = f"{location.lower()}_{timeframe.lower()}_prediction.png"
        try:
            st.image(image_path, caption=f"{location} {timeframe} Prediction", use_column_width=True)
        except FileNotFoundError:
            st.error(f"No prediction available for {location} - {timeframe}.")

st.caption("Updated: May 21, 2025")
