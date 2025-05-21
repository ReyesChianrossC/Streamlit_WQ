import streamlit as st

# Custom HTML & CSS
st.markdown("""
    <style>
        .vertical-box {
            height: 400px;
            width: 100%;
            max-width: 400px;
            margin: 0 auto;
            background-color: #ffffff;
            border: 1.5px solid #d0d0d0;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.06);
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            position: relative;
        }
        .title {
            position: absolute;
            top: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #000000;
        }
        .predict-wrapper, .by-week-wrapper {
            width: 100%;  /* Ensure wrappers span full width of vertical-box */
        }
        .predict-button, .by-week-selector, .location-selector {
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid #ccc;
            background-color: #f9f9f9;
            font-size: 16px;
            cursor: pointer;
            color: #000000;
        }
        .predict-wrapper {
            display: flex;
            justify-content: center;  /* Explicitly center Predict button */
            margin-bottom: 10px;  /* Add spacing between Predict and By Week/Location */
        }
        .by-week-wrapper {
            display: flex;
            flex-direction: row;  /* Arrange By Week and Location selectors side by side */
            align-items: center;  /* Vertically align selectors in the wrapper */
            width: 100%;  /* Ensure wrapper spans full width for proper stretching */
            gap: 10px;  /* Add spacing between By Week and Location selectors */
        }
        .by-week-selector {
            flex-shrink: 0;  /* Prevent By Week selector from shrinking */
            -webkit-appearance: none;  /* Remove default browser styling */
            -moz-appearance: none;
            appearance: none;
            text-align: left;  /* Align text to the left */
        }
        .location-selector {
            flex: 1;  /* Make Location selector occupy remaining horizontal space */
            -webkit-appearance: none;  /* Remove default browser styling */
            -moz-appearance: none;
            appearance: none;
            text-align: left;  /* Align text to the left */
        }
        .predict-button:hover, .by-week-selector:hover, .location-selector:hover {
            background-color: #e0e0e0;
        }
    </style>

    <div class="vertical-box">
        <div class="title">TaalWQ</div>
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
