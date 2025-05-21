import streamlit as st

# Page setup
st.set_page_config(page_title="CNN-LSTM Prediction", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

        .vertical-box {
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
            align-items: center;
            position: relative;
            min-height: 600px; /* Adjusted to fit content comfortably */
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
            width: 100%;
            display: flex;
            justify-content: center;
            z-index: 2;
            margin-bottom: 16px; /* Space below title */
        }
        .title {
            text-align: center;
            font-size: 29px;
            font-weight: 900;
            color: #AFD238;
            text-shadow: 0 0 8px rgba(175, 210, 56, 0.8), 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
            font-family: 'Inter', sans-serif;
        }
        .stat-comparison-container {
            position: absolute;
            top: 16px;
            right: 16px;
            z-index: 2;
        }
        .stat-comparison-button {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            border: 2px solid #00C0D1;
            background: linear-gradient(to bottom, #0082E0, #00C0D1);
            font-size: 16px;
            font-weight: 700;
            color: #E6EFEA;
            text-shadow: 1px 1px 0 #000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', sans-serif;
        }
        .content-wrapper {
            width: 100%;
            z-index: 2;
            padding: 0 16px;
            box-sizing: border-box;
        }
        .stSelectbox, .stButton {
            width: 100%;
            max-width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# BEGIN container within the box
st.markdown('<div class="vertical-box">', unsafe_allow_html=True)
st.markdown('<div class="background-image"></div>', unsafe_allow_html=True)

# Static HTML elements
st.markdown('<div class="stat-comparison-container"><button class="stat-comparison-button">SCI</button></div>', unsafe_allow_html=True)
st.markdown('<div class="title-wrapper"><div class="title">CNN with LSTM Prediction</div></div>', unsafe_allow_html=True)

# Create a Streamlit container that visually stays inside the box
with st.container():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    time_frame = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])
    location = st.selectbox("Select Location", [
        "TANAUAN", "TALISAY", "AYA", "TUMAWAY", "SAMPALOC", "BERINAYAN",
        "BALAKILONG", "BUSO-BUSO", "BAÑAGA", "BILIBINWANG", "SUBIC-ILAYA", "SAN NICOLAS"
    ])

    predict_clicked = st.button("Predict")

    if predict_clicked:
        if time_frame.lower() == "week" and location == "TANAUAN":
            st.image("bar_chart_actual_values.png", caption="Predicted Parameters Chart")
        else:
            st.info(f"No prediction chart available for {location} - {time_frame}.")

    st.markdown('</div>', unsafe_allow_html=True)  # Close content-wrapper
st.markdown('</div>', unsafe_allow_html=True)  # Close vertical-box

# Footer
st.write(f"Last updated: 01:10 PM PST, Wednesday, May 21, 2025")
