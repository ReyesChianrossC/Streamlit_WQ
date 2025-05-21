import streamlit as st

# Custom HTML & CSS with JavaScript
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
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            color: #000000;
            box-shadow: 0 0 10px rgba(0, 130, 224, 0.5);
            font-family: 'Inter', sans-serif;
        }
        .by-week-selector, .location-selector {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            background: linear-gradient(to bottom, #0082E0, #00C0D1);
            font-size: 16px;
            font-weight: 700;
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
            flex-shrink: 0;
        }
        .location-selector {
            flex: 1;
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
        #results {
            margin-top: 20px;
            color: #000000;
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: normal;
            padding: 10px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            display: none;
        }
        .chart-container {
            position: absolute;
            top: 120px;
            width: 100%;
            height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2;
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
        <div class="chart-container">
            <canvas id="prediction-chart"></canvas>
        </div>
        <div class="predict-wrapper">
            <button class="predict-button" id="predict-button">Predict</button>
        </div>
        <div class="by-week-wrapper">
            <select class="by-week-selector" id="by-week-selector">
                <option value="week">Week</option>
                <option value="month">Month</option>
                <option value="year">Year</option>
            </select>
            <select class="location-selector" id="location-selector">
                <option value="TANAUAN">TANAUAN</option>
                <option value="TALISAY">TALISAY</option>
                <option value="AYA">AYA</option>
                <option value="TUMAWAY">TUMAWAY</option>
                <option value="SAMPALOC">SAMPALOC</option>
                <option value="BERINAYAN">BERINAYAN</option>
                <option value="BALAKILONG">BALAKILONG</option>
                <option value="BUSO-BUSO">BUSO-BUSO</option>
                <option value="BAÑAGA">BAÑAGA</option>
                <option value="BILIBINWANG">BILIBINWANG</option>
                <option value="SUBIC-ILAYA">SUBIC-ILAYA</option>
                <option value="SAN NICOLAS">SAN NICOLAS</option>
            </select>
        </div>
        <div id="results"></div>
    </div>

    <script>
        // Load Chart.js library
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => {
            console.log("Chart.js loaded successfully");
            // Initialize chart after script loads
            displayPredictions();
        };
        script.onerror = () => {
            console.error("Failed to load Chart.js");
        };
        document.head.appendChild(script);

        // Load predictions data
        const predictions = [
            {"site": "TANAUAN", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "TANAUAN", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "TANAUAN", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "TALISAY", "time_frame": "Week", "surface_temperature": 26.198494, "middle_temperature": 26.212751, "bottom_temperature": 26.355118, "ph": 8.665811, "ammonia": 0.120792, "nitrate": 0.110559, "phosphate": 2.344637, "dissolved_oxygen": 5.638792, "wqi": 353.236206, "wqi_classification": "Good"},
            {"site": "TALISAY", "time_frame": "Month", "surface_temperature": 26.198494, "middle_temperature": 26.212751, "bottom_temperature": 26.355118, "ph": 8.665811, "ammonia": 0.120792, "nitrate": 0.110559, "phosphate": 2.344637, "dissolved_oxygen": 5.638792, "wqi": 353.236206, "wqi_classification": "Good"},
            {"site": "TALISAY", "time_frame": "Year", "surface_temperature": 26.198494, "middle_temperature": 26.212751, "bottom_temperature": 26.355118, "ph": 8.665811, "ammonia": 0.120792, "nitrate": 0.110559, "phosphate": 2.344637, "dissolved_oxygen": 5.638792, "wqi": 353.236206, "wqi_classification": "Good"},
            {"site": "AYA", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "AYA", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "AYA", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "TUMAWAY", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "TUMAWAY", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "TUMAWAY", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SAMPALOC", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SAMPALOC", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SAMPALOC", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BERINAYAN", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BERINAYAN", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BERINAYAN", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BALAKILONG", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BALAKILONG", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BALAKILONG", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BUSO-BUSO", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BUSO-BUSO", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BUSO-BUSO", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BAÑAGA", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BAÑAGA", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BAÑAGA", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BILIBINWANG", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BILIBINWANG", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "BILIBINWANG", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SUBIC-ILAYA", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SUBIC-ILAYA", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SUBIC-ILAYA", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SAN NICOLAS", "time_frame": "Week", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178986, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SAN NICOLAS", "time_frame": "Month", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780165, "ph": 8.233041, "ammonia": 0.224652, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178985, "wqi": 238.272095, "wqi_classification": "Good"},
            {"site": "SAN NICOLAS", "time_frame": "Year", "surface_temperature": 26.945187, "middle_temperature": 26.868622, "bottom_temperature": 26.780167, "ph": 8.233041, "ammonia": 0.224654, "nitrate": 0.135936, "phosphate": 2.348414, "dissolved_oxygen": 2.178987, "wqi": 238.272095, "wqi_classification": "Good"}
        ];

        // Initialize Chart.js chart
        let chartInstance = null;
        const ctx = document.getElementById('prediction-chart').getContext('2d');

        function updateChart(prediction) {
            console.log("Updating chart for:", prediction.site, prediction.time_frame);
            try {
                // Destroy existing chart if it exists
                if (chartInstance) {
                    chartInstance.destroy();
                }

                // Create new chart
                chartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: [
                            'Surface Temp (°C)', 'Middle Temp (°C)', 'Bottom Temp (°C)', 'pH',
                            'Ammonia (mg/L)', 'Nitrate (mg/L)', 'Phosphate (mg/L)', 'Dissolved Oxygen (mg/L)', 'WQI'
                        ],
                        datasets: [{
                            label: 'Values',
                            data: [
                                prediction.surface_temperature,
                                prediction.middle_temperature,
                                prediction.bottom_temperature,
                                prediction.ph,
                                prediction.ammonia,
                                prediction.nitrate,
                                prediction.phosphate,
                                prediction.dissolved_oxygen,
                                prediction.wqi
                            ],
                            backgroundColor: [
                                '#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1',
                                '#955251', '#B565A7', '#009B77', '#DD4124'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Values'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Parameters'
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            },
                            title: {
                                display: true,
                                text: `Prediction for ${prediction.site} (Month)`
                            }
                        }
                    }
                });
                console.log("Chart updated successfully");
            } catch (error) {
                console.error("Error updating chart:", error);
            }
        }

        // Function to display predictions and update chart
        function displayPredictions() {
            const timeFrame = document.getElementById('by-week-selector').value;
            const location = document.getElementById('location-selector').value;
            const resultsDiv = document.getElementById('results');

            console.log("Display predictions called. Time Frame:", timeFrame, "Location:", location);

            if (timeFrame === 'month') {
                console.log("Looking for prediction. Site:", location, "Time Frame: Month");
                const prediction = predictions.find(p => p.site === location && p.time_frame === 'Month');
                if (prediction) {
                    console.log("Prediction found:", prediction);
                    // Update the chart
                    updateChart(prediction);

                    // Update the results div
                    resultsDiv.style.display = 'block';
                    resultsDiv.innerHTML = `
                        <h4>Predictions for ${location} (Month)</h4>
                        <p>Surface Temp: ${prediction.surface_temperature.toFixed(2)}°C</p>
                        <p>Middle Temp: ${prediction.middle_temperature.toFixed(2)}°C</p>
                        <p>Bottom Temp: ${prediction.bottom_temperature.toFixed(2)}°C</p>
                        <p>pH: ${prediction.ph.toFixed(2)}</p>
                        <p>Ammonia: ${prediction.ammonia.toFixed(2)} mg/L</p>
                        <p>Nitrate: ${prediction.nitrate.toFixed(2)} mg/L</p>
                        <p>Phosphate: ${prediction.phosphate.toFixed(2)} mg/L</p>
                        <p>Dissolved Oxygen: ${prediction.dissolved_oxygen.toFixed(2)} mg/L</p>
                        <p>WQI: ${prediction.wqi.toFixed(2)} (${prediction.wqi_classification})</p>
                    `;
                } else {
                    console.log("No prediction found for", location, "Month");
                    resultsDiv.style.display = 'block';
                    resultsDiv.innerHTML = `<p>No data available for ${location} (Month)</p>`;
                    if (chartInstance) {
                        chartInstance.destroy();
                    }
                }
            } else {
                console.log("Time frame is not 'month'. Hiding results and chart.");
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `<p>Please select "Month" to view predictions.</p>`;
                if (chartInstance) {
                    chartInstance.destroy();
                }
            }
        }

        // Add event listeners
        const predictButton = document.getElementById('predict-button');
        const byWeekSelector = document.getElementById('by-week-selector');
        const locationSelector = document.getElementById('location-selector');

        if (predictButton) {
            predictButton.addEventListener('click', () => {
                console.log("Predict button clicked");
                displayPredictions();
            });
        } else {
            console.error("Predict button not found");
        }

        if (byWeekSelector) {
            byWeekSelector.addEventListener('change', () => {
                console.log("Time frame changed to:", byWeekSelector.value);
                displayPredictions();
            });
        } else {
            console.error("By-week selector not found");
        }

        if (locationSelector) {
            locationSelector.addEventListener('change', () => {
                console.log("Location changed to:", locationSelector.value);
                displayPredictions();
            });
        } else {
            console.error("Location selector not found");
        }
    </script>
""", unsafe_allow_html=True)
