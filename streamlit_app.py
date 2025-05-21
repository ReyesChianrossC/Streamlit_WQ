import streamlit as st

# Custom HTML & CSS
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
            top: 70px;
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
        .stat-comparison-container {
            position: absolute;
            top: 24px;
            right: 24px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
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
            cursor: pointer;
            color: #E6EFEA;
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0;
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5);
            font-family: 'Inter', sans-serif;
        }
        .predict-wrapper, .by-week-wrapper {
            width: 100%;
            z-index: 2;
        }
        .predict-button {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            background: linear-gradient(to bottom, #0082E0, #00C0D1);
            font-size: 19px;
            font-weight: normal;
            cursor: pointer;
            color: #000000;
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5);
            font-family: 'Inter', sans-serif;
            width: 150px; /* Adjusted width */
        }
        .by-week-selector, .location-selector {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            background: linear-gradient(to bottom, #0082E0, #00C0D1);
            font-size: 19px;
            font-weight: normal;
            cursor: pointer;
            color: #000000;
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5);
            font-family: 'Inter', sans-serif;
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            text-align: left;
        }
        .by-week-selector {
            width: 100px; /* Adjusted width */
        }
        .location-selector {
            width: 200px; /* Adjusted width */
        }
        .predict-wrapper {
            display: flex;
            justify-content: center;
            margin-bottom: 12px;
        }
        .by-week-wrapper {
            display: flex;
            flex-direction: row;
            align-items: center;
            width: 100%;
            gap: 12px;
        }
        .stat-comparison-button:hover, .predict-button:hover, .by-week-selector:hover, .location-selector:hover {
            background: linear-gradient(to top, #00C0D1, #0082E0);
            box-shadow: 0 0 15px rgba(0, 130, 224, 0.7);
        }
    </style>

    <div class="vertical-box">
        <div class="background-image"></div>
        <div class="stat-comparison-container">
            <button class="stat-comparison-button">SCI</button>
        </div>
        <div class="title-wrapper">
            <div class="title">CNN with LSTM Prediction</div>
        </div>
        <div class="predict-wrapper">
            <button class="predict-button">Predict</button>
        </div>
        <div class="by-week-wrapper">
            <select class="by-week-selector">
                <option value="week">Week</option>
                <option value="month">Month</option>
                <option value="year">Year</option>
            </select>
            <select class="location-selector">
                <option value="location1">Location 1</option>
                <option value="location2">Location 2</option>
                <option value="location3">Location 3</option>
            </select>
        </div>
    </div>
""", unsafe_allow_html=True)
