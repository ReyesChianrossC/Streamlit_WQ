import streamlit as st

# Custom HTML & CSS
st.markdown("""
    <style>
        .vertical-box {
            height: 480px;
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
            background: radial-gradient(circle, #8000ff, #a100a1, #4b0082); /* Random purple-dominant radial gradient */
            border: 2px solid #8000ff; /* Vibrant purple border */
            border-radius: 14px;
            box-shadow: 0 0 15px rgba(128, 0, 255, 0.6); /* Strong purple glow */
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
            background-image: url('https://github.com/ReyesChianrossC/Streamlit_WQ/blob/main/taal.png'); /* Replace with actual GitHub raw URL */
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
            font-weight: bold;
            color: #a100a1; /* Rich purple for title */
            text-shadow: 0 0 8px rgba(128, 0, 255, 0.8); /* Purple glow effect */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
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
            border: 2px solid #4b0082; /* Dark purple border */
            background: radial-gradient(circle, #8000ff, #a100a1); /* Purple-dominant radial gradient */
            font-size: 16px;
            cursor: pointer;
            color: #ffffff; /* White text for contrast */
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0;
            box-shadow: 0 0 10px rgba(128, 0, 255, 0.5); /* Purple glow */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
        }
        .predict-wrapper, .by-week-wrapper {
            width: 100%; /* Full width of vertical-box */
            z-index: 2; /* Above background image */
        }
        .predict-button {
            padding: 12px 24px;
            border-radius: 10px;
            border: 2px solid #4b0082; /* Dark purple border */
            background: radial-gradient(circle, #8000ff, #a100a1); /* Purple-dominant radial gradient */
            font-size: 19px;
            cursor: pointer;
            color: #ffffff; /* White text for contrast */
            box-shadow: 0 0 10px rgba(128, 0, 255, 0.5); /* Purple glow */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
        }
        .by-week-selector, .location-selector {
            padding: 12px 24px;
            border-radius: 10px;
            border: 2px solid #4b0082; /* Dark purple border */
            background: radial-gradient(circle, #8000ff, #a100a1); /* Purple-dominant radial gradient */
            font-size: 19px;
            cursor: pointer;
            color: #ffffff; /* White text for contrast */
            box-shadow: 0 0 10px rgba(128, 0, 255, 0.5); /* Purple glow */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
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
            background: radial-gradient(circle, #a100a1, #8000ff); /* Reverse purple radial gradient on hover */
            box-shadow: 0 0 15px rgba(128, 0, 255, 0.7); /* Stronger purple glow on hover */
        }
    </style>

    <div class="vertical-box">
        <div class="background-image"></div>
        <div class="stat-comparison-container">
            <button class="stat-comparison-button">SCI</button>
        </div>
        <div class="title-wrapper">
            <div class="title">TaalWQ</div>
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
