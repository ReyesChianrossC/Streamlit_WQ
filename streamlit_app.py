import streamlit as st

# Page setup
st.set_page_config(page_title="CNN-LSTM Prediction", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

        .vertical-box-background {
            position: absolute;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 480px;
            height: 720px;
            background: linear-gradient(to bottom, #0082E0, #00C0D1, #8AE7D4);
            border: 2px solid #0082E0;
            border-radius: 14px;
            box-shadow: 0 0 15px rgba(0, 130, 224, 0.6);
            z-index: -1;
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
            border-radius: 14px;
        }

        .title {
            font-size: 29px;
            font-weight: 900;
            color: #AFD238;
            text-shadow: 0 0 8px rgba(175, 210, 56, 0.8), 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
            font-family: 'Inter', sans-serif;
            text-align: center;
            margin-bottom: 16px;
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
            font-family: 'Inter', sans-serif;
            float: right;
        }
    </style>
""", unsafe_allow_html=True)

# Draw the background box (purely visual layer)
st.markdown("""
    <div class="vertical-box-background">
        <div class="background-image"></div>
    </div>
""", unsafe_allow_html=True)

# Now draw content (which floats visually in front of the box)
st.markdown('<button class="stat-comparison-button">SCI</button>', unsafe_allow_html=True)
st.markdown('<div class="title">CNN with LSTM Prediction</div>', unsafe_allow_html=True)

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

st.write(f"Last updated: 01:10 PM PST, Wednesday, May 21, 2025")
