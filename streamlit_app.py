import streamlit as st

# Custom CSS styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

        .vertical-box {
            height: 480px;
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
            justify-content: flex-end;
            align-items: center;
            position: relative;
            overflow: hidden;
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
            position: absolute;
            top: 30px;
            width: 100%;
            display: flex;
            justify-content: center;
            z-index: 2;
        }

        .title {
            text-align: center;
            font-size: 29px;
            font-weight: 900;
            color: #AFD238;
            text-shadow: 0 0 8px rgba(175, 210, 56, 0.8), 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
            font-family: 'Inter', sans-serif;
        }

        .stat-comparison-button {
            position: absolute;
            top: 24px;
            right: 24px;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            border: 2px solid #00C0D1;
            background: linear-gradient(to bottom, #0082E0, #00C0D1);
            font-size: 16px;
            font-weight: 700;
            color: #E6EFEA;
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', sans-serif;
            z-index: 2;
        }

        .control-wrapper {
            z-index: 2;
            margin-top: 300px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .select-wrapper {
            display: flex;
            gap: 12px;
        }

    </style>
""", unsafe_allow_html=True)

# Container
st.markdown('<div class="vertical-box">', unsafe_allow_html=True)
st.markdown('<div class="background-image"></div>', unsafe_allow_html=True)
st.markdown('<div class="title-wrapper"><div class="title">CNN with LSTM Prediction</div></div>', unsafe_allow_html=True)
st.markdown('<div class="stat-comparison-button">SCI</div>', unsafe_allow_html=True)

# Streamlit widgets
with st.container():
    st.markdown('<div class="control-wrapper">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        time_frame = st.selectbox("Select Time Frame", ["week", "month", "year"], label_visibility="collapsed")
    with col2:
        location = st.selectbox("Select Location", [
            "TANAUAN", "TALISAY", "AYA", "TUMAWAY", "SAMPALOC",
            "BERINAYAN", "BALAKILONG", "BUSO-BUSO", "BAÑAGA",
            "BILIBINWANG", "SUBIC-ILAYA", "SAN NICOLAS"
        ], label_visibility="collapsed")

    show_chart = False
    if st.button("Predict"):
        if time_frame == "week" and location == "TANAUAN":
            show_chart = True

    if show_chart:
        st.image("bar_chart_actual_values.png", use_column_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Close container
st.markdown('</div>', unsafe_allow_html=True)
