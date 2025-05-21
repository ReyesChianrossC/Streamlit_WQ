import streamlit as st

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
        font-family: 'Inter', sans-serif;
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
        text-shadow: 0 0 8px rgba(175, 210, 56, 0.8), 1px 1px 0 #000, -1px -1px 0 #000;
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
        color: #E6EFEA;
        font-weight: 700;
        text-shadow: 1px 1px 0 #000;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2;
    }

    .form-controls {
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 280px;
        gap: 10px;
    }

    select, .fake-button {
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        background: linear-gradient(to bottom, #0082E0, #00C0D1);
        font-size: 16px;
        font-weight: 700;
        color: #000;
        box-shadow: 0 0 10px rgba(0, 130, 224, 0.5);
        font-family: 'Inter', sans-serif;
        cursor: default;
    }

    .checkbox-toggle {
        display: none;
    }

    .fake-button {
        text-align: center;
    }

    .chart-container {
        display: none;
        margin-top: 16px;
    }

    .checkbox-toggle:checked + .fake-button + .chart-container {
        display: block;
    }

</style>

<div class="vertical-box">
    <div class="background-image"></div>

    <div class="stat-comparison-button">SCI</div>

    <div class="title-wrapper">
        <div class="title">CNN with LSTM Prediction</div>
    </div>

    <div class="form-controls">
        <select>
            <option>Week</option>
            <option>Month</option>
            <option>Year</option>
        </select>
        <select>
            <option>TANAUAN</option>
            <option>TALISAY</option>
            <option>AYA</option>
            <option>TUMAWAY</option>
            <option>SAMPALOC</option>
        </select>

        <!-- Simulate interaction -->
        <label>
            <input class="checkbox-toggle" type="checkbox" />
            <div class="fake-button">Predict</div>
            <div class="chart-container">
                <img src="bar_chart_actual_values.png" width="100%" />
            </div>
        </label>
    </div>
</div>
""", unsafe_allow_html=True)
