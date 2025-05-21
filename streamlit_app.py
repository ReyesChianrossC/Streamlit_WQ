import streamlit as st

# CSS for enhanced ultra-compact card style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }

    .container {
        background: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        max-width: 360px;
        margin: 20px auto;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    .stButton>button {
        background: linear-gradient(135deg, #0077cc, #00b7d4);
        color: white;
        font-weight: 600;
        font-size: 0.9em;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        box-shadow: 0 2px 8px rgba(0, 119, 204, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 12px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00b7d4, #0077cc);
        box-shadow: 0 4px 12px rgba(0, 119, 204, 0.5);
        transform: translateY(-1px);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(0, 119, 204, 0.3);
    }

    .stSelectbox>div {
        background: #f8f9fd;
        color: #333;
        font-weight: 600;
        font-size: 0.85em;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0.4em;
        margin-bottom: 12px;
        transition: border-color 0.2s ease;
    }
    .stSelectbox>div:hover, .stSelectbox>div:focus {
        border-color: #0077cc;
    }

    .stCaption {
        text-align: center;
        color: #888;
        font-size: 0.75em;
        font-weight: 400;
        margin-top: 10px;
    }

    h1 {
        font-size: 1.8em;
        font-weight: 700;
        color: #222;
        text-align: center;
        margin-bottom: 20px;
    }

    @media (max-width: 600px) {
        .container {
            max-width: 90%;
            padding: 12px 16px;
        }
        h1 {
            font-size: 1.5em;
        }
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
        with st.spinner("Generating prediction..."):
            image_path = f"{location.lower()}_{timeframe.lower()}_prediction.png"
            try:
                st.image(image_path, caption=f"{location} {timeframe} Prediction", use_column_width=True)
            except FileNotFoundError:
                st.error(f"No prediction available for {location} - {timeframe}.")

st.caption("Updated: May 21, 2025")
