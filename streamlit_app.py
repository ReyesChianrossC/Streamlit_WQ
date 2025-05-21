import streamlit as st
import os

# CSS for enhanced and vibrant design with horizontal belt
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        background: linear-gradient(135deg, #e6f0fa, #b3d4fc);
        height: 100%;
        margin: 0;
    }

    .container {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px 25px;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 40px auto;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .belt {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #007bff, #00c4cc);
        color: white;
        font-weight: 600;
        font-size: 1em;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        box-shadow: 0 3px 10px rgba(0, 123, 255, 0.4);
        transition: all 0.3s ease;
        width: 100%; /* Full width within its own container */
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00c4cc, #007bff);
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.6);
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(0, 123, 255, 0.4);
    }

    .stSelectbox>div {
        background: #ffffff;
        color: #333;
        font-weight: 600;
        font-size: 0.9em;
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 0.5em;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        width: 100%; /* Ensure selectbox takes full column width */
    }
    .stSelectbox>div:hover, .stSelectbox>div:focus {
        border-color: #00c4cc;
        box-shadow: 0 0 10px rgba(0, 196, 204, 0.3);
    }

    h1 {
        font-size: 2.2em;
        font-weight: 700;
        color: #004085;
        text-align: center;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stCaption {
        text-align: center;
        color: #666;
        font-size: 0.8em;
        font-weight: 400;
        margin-top: 15px;
    }

    @media (max-width: 600px) {
        .container {
            max-width: 90%;
            padding: 15px 20px;
            margin: 20px auto;
        }
        h1 {
            font-size: 1.8em;
        }
        .belt {
            flex-direction: column;
            gap: 5px;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("Prediction App", anchor=False)

with st.container():
    # Horizontal belt layout using columns for selectboxes only
    col1, col2 = st.columns([1, 1])  # Equal widths for two selectboxes
    with col1:
        timeframe = st.selectbox("Time Frame", ["Week", "Month", "Year"], key="timeframe")
    with col2:
        location = st.selectbox("Location", [
            "Tanauan", "Talisay", "Aya", "Tumaway", "Sampaloc",
            "Berinayan", "Balakilong", "Buso-Buso", "Bañaga",
            "Bilibinwang", "Subic-Ilaya", "San Nicolas"
        ], key="location")

    # Predict button below the belt
    if st.button("Predict"):
        with st.spinner("Generating prediction..."):
            image_path = f"{location.lower()}_{timeframe.lower()}_prediction.png"
            if os.path.exists(image_path):
                st.image(image_path, caption=f"{location} {timeframe} Prediction", use_container_width=True)
            else:
                fallback_image = "bar_chart_actual_values.png"
                if os.path.exists(fallback_image):
                    st.image(fallback_image, caption=f"Showing actual values for {location} - {timeframe} (Prediction image not found)", use_container_width=True)
                else:
                    st.error(f"No prediction image found for {location} - {timeframe}, and fallback image 'bar_chart_actual_values.png' is missing.")

st.caption("Updated: 02:03 PM PST, Wednesday, May 21, 2025")
