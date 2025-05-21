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
            background: linear-gradient(to bottom, #0082E0, #00C0D1, #8AE7D4); /* Vertical linear gradient: Fiji Blue, Sea Serpent, Seychelles Blue */
            border: 2px solid #0082E0; /* Fiji Blue border */
            border-radius: 14px;
            box-shadow: 0 0 15px rgba(0, 130, 224, 0.6); /* Fiji Blue glow */
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            position: relative;
            overflow: hidden; /* Ensure image doesn't overflow */
        }
        .background-image {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('https://raw.githubusercontent.com/ReyesChianrossC/Streamlit_WQ/main/taal.png'); /* Taal image from GitHub */
            background-size: cover;
            background-position: center;
            opacity: 0.1; /* Very low opacity */
            z-index: 1; /* Above gradient, below content */
        }
        .title-wrapper {
            position: absolute;
            top: 70px; /* Position below stat-comparison-container */
            width: 100%;
            display: flex;
            justify-content: center; /* Center the title horizontally */
            z-index: 2; /* Above background image */
        }
        .title {
            text-align: center;
            font-size: 29px;
            font-weight: 900; /* Bolder for contrast */
            color: #AFD238; /* Atlantis Green for title */
            text-shadow: 0 0 8px rgba(175, 210, 56, 0.8), 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000; /* Green glow with black border outline */
            font-family: 'Inter', sans-serif; /* Inter font */
        }
        .stat-comparison-container {
            position: absolute;
            top: 24px;
            right: 24px;
            display: flex;
            flex-direction: column;
            align-items: flex-end; /* Align button to the right */
            z-index: 2; /* Above background image */
        }
        .stat-comparison-button {
            width: 40px; /* 1x1 square */
            height: 40px;
            border-radius: 10px;
            border: 2px solid #00C0D1; /* Sea Serpent border */
            background: linear-gradient(to bottom, #0082E0, #00C0D1); /* Vertical linear gradient: Fiji Blue to Sea Serpent */
            font-size: 16px;
            font-weight: 700; /* Bold for contrast */
            cursor: pointer;
            color: #E6EFEA; /* Gray Tint for high contrast */
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000; /* Black border outline */
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0;
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5); /* Fiji Blue glow */
            font-family: 'Inter', sans-serif; /* Inter font */
        }
        .predict-wrapper, .by-week-wrapper {
            width: 100%; /* Full width of vertical-box */
            z-index: 2; /* Above background image */
        }
        .predict-button {
            padding: 12px 24px;
            border-radius: 10px;
            border: 2px solid #00C0D1; /* Sea Serpent border */
            background: linear-gradient(to bottom, #0082E0, #00C0D1); /* Vertical linear gradient: Fiji Blue to Sea Serpent */
            font-size: 19px;
            font-weight: 700; /* Bold for contrast */
            cursor: pointer;
            color: #E6EFEA; /* Gray Tint for high contrast */
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000; /* Black border outline */
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5); /* Fiji Blue glow */
            font-family: 'Inter', sans-serif; /* Inter font */
        }
        .by-week-selector, .location-selector {
            padding: 12px 24px;
            border-radius: 10px;
            border: 2px solid #00C0D1; /* Sea Serpent border */
            background: linear-gradient(to bottom, #0082E0, #00C0D1); /* Vertical linear gradient: Fiji Blue to Sea Serpent */
            font-size: 19px;
            font-weight: 700; /* Bold for contrast */
            cursor: pointer;
            color: #333333; /* Dark gray for better contrast */
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000; /* Black border outline */
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5); /* Fiji Blue glow */
            font-family: 'Inter', sans-serif; /* Inter font */
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            text-align: left;
        }
        .by-week-selector {
            flex-shrink: 0; /* Prevent shrinking */
        }
        .location-selector {
            flex: 1; /* Occupy remaining space */
        }
        .predict-wrapper {
            display: flex;
            justify-content: center; /* Center Predict button */
            margin-bottom: 12px; /* Spacing */
        }
        .by-week-wrapper {
            display: flex;
            flex-direction: row; /* Side-by-side selectors */
            align-items: center; /* Vertically align */
            width: 100%;
            gap: 12px; /* Spacing between selectors */
        }
        .stat-comparison-button:hover, .predict-button:hover, .by-week-selector:hover, .location-selector:hover {
            background: linear-gradient(to top, #00C0D1, #0082E0); /* Reverse vertical gradient on hover */
            box-shadow: 0 0 15px rgba(0, 130, 224, 0.7); /* Stronger Fiji Blue glow on hover */
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
