import streamlit as st

# Custom HTML & CSS
st.markdown("""
    <style>
        .vertical-box {
            height: 480px;
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
            background: linear-gradient(135deg, #00ff00, #39ff14, #00cc00); /* Neon green gradient */
            border: 2px solid #00ff00; /* Neon green border */
            border-radius: 14px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.5); /* Neon glow effect */
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            position: relative;
        }
        .title-wrapper {
            position: absolute;
            top: 70px; /* Position below stat-comparison-container */
            width: 100%;
            display: flex;
            justify-content: center; /* Center the title horizontally */
        }
        .title {
            text-align: center;
            font-size: 29px;
            font-weight: bold;
            color: #00ff00; /* Neon green for title */
            text-shadow: 0 0 8px rgba(0, 255, 0, 0.7); /* Retro glow effect */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
        }
        .stat-comparison-container {
            position: absolute;
            top: 24px;
            right: 24px;
            display: flex;
            flex-direction: column;
            align-items: flex-end; /* Align button to the right */
        }
        .stat-comparison-button {
            width: 40px; /* 1x1 square */
            height: 40px;
            border-radius: 10px;
            border: 2px solid #00cc00; /* Slightly darker neon green border */
            background: linear-gradient(135deg, #39ff14, #00ff00); /* Gradient for button */
            font-size: 16px;
            cursor: pointer;
            color: #000000; /* Black text for contrast */
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.4); /* Neon glow */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
        }
        .predict-wrapper, .by-week-wrapper {
            width: 100%; /* Full width of vertical-box */
        }
        .predict-button {
            padding: 12px 24px;
            border-radius: 10px;
            border: 2px solid #00cc00; /* Neon green border */
            background: linear-gradient(135deg, #39ff14, #00ff00); /* Gradient for button */
            font-size: 19px;
            cursor: pointer;
            color: #000000; /* Black text for contrast */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.4); /* Neon glow */
            font-family: 'Courier New', Courier, monospace; /* Retro font */
        }
        .by-week-selector, .location-selector {
            padding: 12px 24px;
            border-radius: 10px;
            border: 2px solid #00cc00; /* Neon green border */
            background: linear-gradient(135deg, #39ff14, #00ff00); /* Gradient for selectors */
            font-size: 19px;
            cursor: pointer;
            color: #000000; /* Black text for contrast */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.4); /* Neon glow */
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
            background: linear-gradient(135deg, #00cc00, #39ff14); /* Reverse gradient on hover */
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.6); /* Stronger glow on hover */
        }
    </style>

    <div class="vertical-box">
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
